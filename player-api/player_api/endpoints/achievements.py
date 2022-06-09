from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from player_api.db import Challenges, ChallengeClasses
from player_api.middlewares import get_db
from player_api.models.achievements import Achievements, AchievementCategory, Achievement, AchievementStats
from player_api.models.player import PlayerId, TierEnum

router = APIRouter()


@router.get(
    "/achievements",
    response_model=Achievements,
)
def get_achievements(
    puuids: list[PlayerId] | None, rank: TierEnum | None, champion: str | None, user: str, db: Session = Depends(get_db)
):
    user_puuid = user
    user_challenges: list[Challenges] = db.query(Challenges).join(ChallengeClasses).where(Challenges.summoner_id == user_puuid).all()

    challenge_categories: dict[str, dict[str, _YouOther]] = {}
    for challenge in user_challenges:
        category = challenge.challenge_class.name
        if category not in challenge_categories:
            challenge_categories[category] = {}
        if challenge.name not in challenge_categories[category]:
            challenge_categories[category][challenge.name] = _YouOther(you=None, other=None, description=challenge.challenge_class.description)
        challenge_categories[category][challenge.name].you = _Stats(max=challenge.highscore, total=challenge.total, avg=challenge.average_per_game)

    # TODO: other

    return Achievements(
        items=[
            AchievementCategory(category=cat_name, achievements=[Achievement(fav=False, name=ac_name, description=ac_value.description, you=AchievementStats()) for ac_name, ac_value in cat_value.items()]) for cat_name, cat_value in challenge_categories.items()
        ]
    )


class _Stats(BaseModel):
    max: float
    total: float
    avg: float


class _YouOther(BaseModel):
    you: _Stats | None
    other: _Stats | None
    description: str
