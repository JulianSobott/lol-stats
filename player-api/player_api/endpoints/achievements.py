from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from player_api.db import Challenges, ChallengeClasses, Summoners
from player_api.middlewares import get_db
from player_api.models.achievements import (
    Achievements,
    AchievementCategory,
    Achievement,
    AchievementStats,
    AchievementStat, Comparison,
)
from player_api.models.player import PlayerId, TierEnum
from player_api.models.responses import ExceptionMessage

router = APIRouter()
EPSILON = 0.00001

@router.get(
    "/achievements",
    response_model=Achievements,
    responses={204: {"description": "Filter didn't match any challenges"}},
)
def get_achievements(
    puuids: list[PlayerId] = Query(default=[]),
    rank: TierEnum | None = None,
    champion: str | None = None,
    user: str | None = None,
    db: Session = Depends(get_db),
):
    user_puuid = user
    user_challenges: list[Challenges] = (
        db.query(Challenges)
        .where(Challenges.summoner_id == user_puuid)
        .order_by(Challenges.name)
        .all()
    )
    criterion = [
        Challenges.summoner_id != user_puuid,
    ]
    if puuids:
        criterion.append(Challenges.summoner_id.in_(puuids))
    if rank and rank != "*":
        criterion.append(Summoners.tier == rank)
    if champion and champion != "*":
        pass  # TODO: filter for champions. Currently all games had to be loaded

    other_challenges: list[Challenges] = (
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

    if len(other_challenges) == 0:
        raise HTTPException(status_code=204)

    assert len(other_challenges) == len(user_challenges), (
        f"For comparison, both need to have same number of challenges. "
        f"{len(other_challenges)=} {len(user_challenges)=}"
    )

    challenge_classes: list[ChallengeClasses] = db.query(ChallengeClasses).all()
    classes_lookup: dict[str, ChallengeClasses] = {
        c.name: c for c in challenge_classes
    }

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
                fav=False,
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


def _compare(*, user: float, other: float, operator: str) -> _CompareResult:
    cmp_funcs = {"<": float.__lt__, ">": float.__gt__}
    if abs(user - other) < EPSILON:
        return _CompareResult(user=Comparison.EQUAL, other=Comparison.EQUAL)
    res = cmp_funcs[operator](user, other)
    if res:
        return _CompareResult(user=Comparison.BETTER, other=Comparison.WORSE)
    else:
        return _CompareResult(user=Comparison.WORSE, other=Comparison.BETTER)
