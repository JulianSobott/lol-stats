import asyncio

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, asc
import random

from player_api.db import ChallengeClasses, Challenges, Summoners
from player_api.log import get_logger
from player_api.middlewares import get_async_db
from player_api.models.leaderboards import Leaderboards, Challenge, LeaderboardPlayer

router = APIRouter()
logger = get_logger(__name__)

DEFAULT_NUM_LEADERBOARDS = 3
DEFAULT_NUM_PLAYERS = 5


@router.get(
    "/achievements/leaderboards",
    response_model=Leaderboards,
    responses={204: {"description": "Filter didn't match any challenges"}},
)
async def get_leaderboards(
    num_challenges: int = Query(DEFAULT_NUM_LEADERBOARDS, alias="challenges"),
    num_players: int = Query(DEFAULT_NUM_PLAYERS, alias="players"),
    db: AsyncSession = Depends(get_async_db),
):
    challenges = await _get_random_challenges(db, n=num_challenges)
    return Leaderboards(
        challenges=[
            Challenge(
                name=challenge.name,
                players=await _get_top_players(db, challenge=challenge, n=num_players),
            )
            for challenge in challenges
        ]
    )


async def _get_random_challenges(
    db: AsyncSession, n: int
) -> list["_SelectedChallenge"]:
    q = select(ChallengeClasses.name, ChallengeClasses.comparison_operator, ChallengeClasses.description)
    all_challenges = list((await db.execute(q)))
    selected_challenges = random.choices(all_challenges, k=n)
    return [
        _SelectedChallenge(name=row.description, comparator=row.comparison_operator, id=row.name)
        for row in selected_challenges
    ]


async def _get_top_players(
    db: AsyncSession, challenge: "_SelectedChallenge", n: int
) -> list[LeaderboardPlayer]:
    cmp = desc if challenge.comparator == ">" else asc
    q = (
        select(
            Summoners.puuid,
            Summoners.name,
            Summoners.icon_path,
            Challenges.average_per_game,
        )
        .join(Summoners)
        .where(Challenges.name == challenge.id, Summoners.last_update.is_not(None))
        .order_by(cmp(Challenges.average_per_game))
        .limit(n)
    )
    res = await db.execute(q)
    return [
        LeaderboardPlayer(
            id=row.puuid,
            name=row.name,
            player_icon_path=row.icon_path,
            value=row.average_per_game,
        )
        for row in res
    ]


class _SelectedChallenge(BaseModel):
    id: str
    name: str
    comparator: str
