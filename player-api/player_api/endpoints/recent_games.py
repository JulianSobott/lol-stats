import json
from datetime import datetime
from urllib.parse import urlencode

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.requests import Request

from player_api.db import datetime_to_db, Games, db_to_datetime
from player_api.get_player import get_player_by_id
from player_api.log import get_logger
from player_api.middlewares import get_db
from player_api.models.game import (
    Page,
    Game,
    PlayerStats,
    TeamMember,
    Champion,
    GamePlayer,
    TeamSide,
)
from player_api.models.player import PlayerId
from player_api.models.responses import ExceptionMessage
from player_api.riot_api import find_player_in_riot_api_by, SearchTerm

DEFAULT_GAMES_PER_PAGE = 5


router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/players/{player_id}/recent-games",
    response_model=Page[Game],
    responses={404: {"model": ExceptionMessage, "description": "Player not found"}},
)
async def recent_games(
    player_id: PlayerId,
    request: Request,
    start_before: datetime = None,
    limit: int = DEFAULT_GAMES_PER_PAGE,
    db: Session = Depends(get_db),
):
    logger.debug(f"method=recent_games {player_id=}")
    player = get_player_by_id(db, player_id)
    if player is None:
        riot_player = find_player_in_riot_api_by(player_id, SearchTerm.id)
        if riot_player:
            logger.debug(
                f"method=recent_games {player_id=} msg='player not in DB, but found in Riot API'"
            )
            return Page[Game](items=[], next="")
        raise HTTPException(status_code=404, detail="player not found")
    logger.debug(f"method=recent_games {player_id=} {player.name=}")
    if start_before is None:
        start_before = datetime(2090, 1, 1)
    games = await query_games(db, limit, player.puuid, start_before)
    if len(games) == 0:
        return Page[Game](items=[], next="")
    next_link = await compute_next_link(games, limit, request)
    ret_games = []
    # TODO: run concurrently and benchmark
    for game in games:
        ret_game = await compute_game(db, game, player_id)
        if ret_game is not None:
            ret_games.append(ret_game)
    return Page[Game](items=ret_games, next=str(next_link))


async def compute_next_link(games: list[Games], limit: int, request: Request):
    next_start_before = db_to_datetime(games[-1].start_time).isoformat()
    next_link = (
        str(request.url.path)
        + "?"
        + urlencode({"start_before": next_start_before, "limit": limit})
    )
    return next_link


async def query_games(
    db: Session, limit: int, player_id: PlayerId, start_before: datetime
) -> list[Games]:
    start_before = datetime_to_db(start_before)
    games: list[Games] = (
        db.query(Games)
        .where(Games.summoner_id == player_id, Games.start_time < start_before)
        .order_by(desc(Games.start_time))
        .limit(limit)
        .all()
    )
    return games


async def compute_game(db: Session, game: Games, player_id: PlayerId) -> Game | None:
    games_of_team: list[Games] = (
        db.query(Games).where(Games.match_id == game.match_id).all()
    )
    if len(games_of_team) != 10:
        logger.warning(
            f"Game has not imported stats for all players. match_id={game.match_id}"
        )
        return None

    ally_team = []
    enemy_team = []
    self = None
    win = False
    for player_game in games_of_team:
        all_stats = json.loads(player_game.challenges)
        stats = PlayerStats(
            kills=all_stats["-kills"],
            deaths=all_stats["-deaths"],
            assists=all_stats["-assists"],
            creep_score=all_stats["-totalMinionsKilled"],
        )
        team_member = TeamMember(
            champion=Champion(
                name=player_game.champion.name,
                icon_path=player_game.champion.icon_path,
            ),
            player=GamePlayer(
                id=player_game.summoner.puuid, name=player_game.summoner.name
            ),
            stats=stats,
            team=player_game.team,
            lane=player_game.lane,
        )
        if player_game.team == game.team:
            ally_team.append(team_member)
        else:
            enemy_team.append(team_member)
        if player_game.summoner.puuid == player_id:
            self = team_member
            win = player_game.win

    assert self is not None, "Own player not appeared in games"
    return Game(
        match_id=game.match_id,
        victorious_team=TeamSide.red
        if (self.team == TeamSide.red and win)
        or (self.team == TeamSide.blue and not win)
        else TeamSide.blue,
        ally_team=_order_members(ally_team),
        enemy_team=_order_members(enemy_team),
        duration=game.duration,
        timestamp=db_to_datetime(game.start_time),
        self=self,
        win=win,
    )


def _order_members(members: list[TeamMember]) -> list[TeamMember]:
    position_order = {
        "TOP_LANE": 0,
        "JUNGLE": 1,
        "MID_LANE": 2,
        "BOT_LANE": 3,
        "UTILITY": 4,
    }
    return sorted(members, key=lambda m: position_order.get(m.lane, 5))
