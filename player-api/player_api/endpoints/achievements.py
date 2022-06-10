from enum import Enum

import requests
from fastapi import APIRouter, Depends, Query, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from player_api.db import Challenges, ChallengeClasses, Summoners
from player_api.log import get_logger
from player_api.middlewares import get_db
from player_api.models.achievements import (
    Achievements,
    AchievementCategory,
    Achievement,
    AchievementStats,
    AchievementStat,
    Comparison,
)
from player_api.models.player import PlayerId, TierEnum, UserId

router = APIRouter()
EPSILON = 0.00001
logger = get_logger(__name__)


class CompareGroup(str, Enum):
    FRIEND = "friend"
    PLAYER = "player"
    GLOBAL = "global"


@router.get(
    "/achievements",
    response_model=Achievements,
    responses={204: {"description": "Filter didn't match any challenges"}},
)
def get_achievements(
    me: str,
    is_gloabal: bool = Query(default=False, alias="global"),
    competitor_id: list[UserId] = Query(default=[]),
    competitor: PlayerId | None = None,
    rank: TierEnum | str | None = None,
    champion: str | None = None,
    db: Session = Depends(get_db),
):
    user = _get_user_data(me)
    user_challenges = _query_achievements(
        db, [Challenges.summoner_id == user.player_uuid]
    )

    criterion = [
        Challenges.summoner_id != user.player_uuid,
    ]
    if is_gloabal:  # global
        pass
    elif competitor_id:     # friends
        friends_puuids = []
        for competitor in competitor_id:
            res = _get_user_data(competitor)
            friends_puuids.append(res.player_uuid)
        criterion.append(Challenges.summoner_id.in_(friends_puuids))
    elif competitor:    # player
        criterion.append(Challenges.summoner_id == competitor)

    if rank and rank != "*":
        criterion.append(Summoners.tier == rank)
    if champion and champion != "*":
        pass  # TODO: filter for champions. Currently all games had to be loaded
    other_challenges = _query_achievements(db, criterion)

    if len(other_challenges) == 0:
        raise HTTPException(status_code=204)

    assert len(other_challenges) == len(user_challenges), (
        f"For comparison, both need to have same number of challenges. "
        f"{len(other_challenges)=} {len(user_challenges)=}"
    )

    challenge_classes = _query_challenge_classes(db)
    classes_lookup: dict[str, ChallengeClasses] = {c.name: c for c in challenge_classes}
    fav_challenges = _get_favourite_challenges(user)

    challenge_categories: dict[str, list[Achievement]] = {}
    for i in range(len(user_challenges)):
        user_challenge = user_challenges[i]
        other_challenge = other_challenges[i]
        challenge_class = classes_lookup[other_challenge.name]
        if challenge_class.class_name not in challenge_categories:
            challenge_categories[challenge_class.class_name] = []
        max_cmp = _compare(
            user=user_challenge.highscore,
            other=other_challenge.highscore,
            operator=challenge_class.comparison_operator,
        )
        total_cmp = _compare(
            user=user_challenge.total,
            other=other_challenge.total,
            operator=challenge_class.comparison_operator,
        )
        avg_cmp = _compare(
            user=user_challenge.average_per_game,
            other=other_challenge.average_per_game,
            operator=challenge_class.comparison_operator,
        )
        challenge_categories[challenge_class.class_name].append(
            Achievement(
                fav=challenge_class.name in fav_challenges,
                name=challenge_class.name,
                description=challenge_class.description,
                you=AchievementStats(
                    max=AchievementStat(
                        value=user_challenge.highscore, compare=max_cmp.user
                    ),
                    total=AchievementStat(
                        value=user_challenge.total, compare=total_cmp.user
                    ),
                    avg=AchievementStat(
                        value=user_challenge.average_per_game, compare=avg_cmp.user
                    ),
                ),
                other=AchievementStats(
                    max=AchievementStat(
                        value=other_challenge.highscore, compare=max_cmp.other
                    ),
                    total=AchievementStat(
                        value=other_challenge.total, compare=total_cmp.other
                    ),
                    avg=AchievementStat(
                        value=other_challenge.average_per_game, compare=avg_cmp.other
                    ),
                ),
            )
        )

    return Achievements(
        items=[
            AchievementCategory(category=cat_name, achievements=cat_value)
            for cat_name, cat_value in challenge_categories.items()
        ]
    )


class _CompareResult(BaseModel):
    user: Comparison
    other: Comparison


class _UserInfo(BaseModel):
    id: str
    player_uuid: str
    region: str


def _compare(*, user: float, other: float, operator: str) -> _CompareResult:
    cmp_funcs = {"<": float.__lt__, ">": float.__gt__}
    if abs(user - other) < EPSILON:
        return _CompareResult(user=Comparison.EQUAL, other=Comparison.EQUAL)
    res = cmp_funcs[operator](user, other)
    if res:
        return _CompareResult(user=Comparison.BETTER, other=Comparison.WORSE)
    else:
        return _CompareResult(user=Comparison.WORSE, other=Comparison.BETTER)


def _query_achievements(db: Session, criterion: list) -> list[Challenges]:
    return (
        db.query(
            Challenges.name,
            func.avg(Challenges.total).label("total"),
            func.avg(Challenges.highscore).label("highscore"),
            func.avg(Challenges.average_per_game).label("average_per_game"),
        )
        .join(Summoners)
        .where(*criterion)
        .group_by(Challenges.name)
        .order_by(Challenges.name)
        .all()
    )


def _query_challenge_classes(db: Session) -> list[ChallengeClasses]:
    return db.query(ChallengeClasses).all()


def _get_favourite_challenges(user: _UserInfo) -> set[str]:
    return set()    # TODO: remove when endpoint is deployed
    res = requests.get(f"https://lol-stats.de/api/users/{user.id}/achievements")
    if not res.ok:
        logger.warn(
            f"method=_get_user_data msg='request returned error code' "
            f"{res.status_code=} {res.text} {user=}"
        )
        raise HTTPException(res.status_code, detail=res.text)
    return set(res.json()["achievements"])


def _get_user_data(user_id: str):
    res = requests.get(f"https://lol-stats.de/api/users/{user_id}")
    if not res.ok:
        logger.warn(
            f"method=_get_user_data msg='request returned error code' "
            f"{res.status_code=} {res.text} {user_id=}"
        )
        raise HTTPException(res.status_code, detail=res.text)
    return _UserInfo(**res.json())
