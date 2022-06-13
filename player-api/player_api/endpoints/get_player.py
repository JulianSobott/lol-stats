import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, case, text
from sqlalchemy.orm import Session

from player_api.db import Games, Champions
from player_api.get_player import get_player_by_id
from player_api.import_state import is_player_imported
from player_api.log import get_logger
from player_api.middlewares import get_db
from player_api.models.player import Player, PlayerId, MostPlayed, Rank, TierEnum
from player_api.models.responses import ExceptionMessage
from player_api.riot_api import find_player_in_riot_api_by, SearchTerm

DEFAULT_NUM_MOST_PLAYED_CHAMPS = 3

router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/players/{player_id}",
    response_model=Player,
    responses={404: {"model": ExceptionMessage, "description": "Player not found"}},
)
async def get_player(player_id: PlayerId, db: Session = Depends(get_db)):
    """Get a player by riots puuid"""
    logger.debug(f"method=get_player {player_id=}")
    if not is_player_imported(db, player_id):
        player = find_player_in_riot_api_by(player_id, SearchTerm.id)
        if player:
            logger.debug(
                f'method=get_player msg="found player in riot API" {player.name=}'
            )
            return Player(
                id=player.id,
                player_icon_path=player.player_icon_path,
                name=player.name,
                win_rate=None,
                level=player.level,
                rank=None,
                most_played=None,
                imported=False,
            )
        else:
            raise HTTPException(status_code=404, detail="player not found")

    player = get_player_by_id(db, player_id)
    logger.debug(f"method=get_player {player_id=} {player.name=}")

    most_played, win_rate = await asyncio.gather(
        query_most_played(db, player.puuid), query_win_rate(db, player.puuid)
    )

    logger.debug(f"method=get_player {most_played=}")
    logger.debug(f"method=get_player {win_rate=}")

    rank = Rank.from_summoner(player)
    return Player(
        id=player.puuid,
        player_icon_path=player.icon_path,
        name=player.name,
        level=player.level,
        rank=rank,
        most_played=most_played,
        win_rate=win_rate,
        imported=True,
    )


async def query_win_rate(db: Session, player_id: PlayerId) -> int:
    result = (
        db.query(
            func.count(Games.summoner_id).label("num_played"),
            func.count(case([(Games.win, 1)])).label("won"),
        )
        .where(Games.summoner_id == player_id)
        .first()
    )
    win_rate = calc_win_rate(result.num_played, result.won)
    return win_rate


async def query_most_played(db: Session, player_id: PlayerId) -> list[MostPlayed]:
    most_played_db = (
        db.query(
            Games.champ_id,
            Champions.name,
            Champions.icon_path,
            func.count(Games.champ_id).label("num_played"),
            func.count(case([(Games.win, 1)])).label("won"),
        )
        .join(Champions)
        .where(Games.summoner_id == player_id)
        .group_by(Games.champ_id, Champions.name, Champions.icon_path)
        .order_by(text("num_played DESC"))
        .limit(DEFAULT_NUM_MOST_PLAYED_CHAMPS)
        .all()
    )
    most_played = []
    for champ in most_played_db:
        most_played.append(
            MostPlayed(
                champion_id=champ[0],
                champion_name=champ[1],
                icon_path=champ[2],
                games=champ[3],
                win_rate=calc_win_rate(games=champ[3], won=champ[4]),
            )
        )
    return most_played


def calc_win_rate(games: int, won: int) -> int:
    if won == 0:
        return 0
    if won > games:
        raise ValueError(f"Won more games than played. {games=} {won=}")
    return int((won / games) * 100)
