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

DEFAULT_GAMES_PER_PAGE = 5


router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/players/{player_id}/recent-games",
    response_model=Page[Game],
    responses={404: {"model": ExceptionMessage, "description": "Player not found"}},
)
def recent_games(
    player_id: PlayerId,
    request: Request,
    start_before: datetime = None,
    limit: int = DEFAULT_GAMES_PER_PAGE,
    db: Session = Depends(get_db),
):
    logger.debug(f"method=recent_games {player_id=}")
    player = get_player_by_id(db, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="player not found")
    logger.debug(f"method=recent_games {player_id=} {player.name=}")
    if start_before is None:
        start_before = datetime(2090, 1, 1)
    start_before = datetime_to_db(start_before)
    games: list[Games] = (
        db.query(Games)
        .where(Games.summoner_id == player.puuid, Games.start_time < start_before)
        .order_by(desc(Games.start_time))
        .limit(limit)
        .all()
    )
    if len(games) == 0:
        return Page[Game](items=[], next="")
    next_start_before = db_to_datetime(games[-1].start_time).isoformat()
    next_link = (
        str(request.url.path)
        + "?"
        + urlencode({"start_before": next_start_before, "limit": limit})
    )
    ret_games = []
    for game in games:
        games_of_team: list[Games] = (
            db.query(Games).where(Games.match_id == game.match_id).all()
        )
        if len(games_of_team) != 10:
            logger.warning(
                f"Game has not imported stats for all players. match_id={game.match_id}"
            )
            continue

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
                team=TeamSide.red if game.team == TeamSide.red.value else TeamSide.blue,
            )
            if player_game.team == game.team:
                ally_team.append(team_member)
            else:
                enemy_team.append(team_member)
            if player_game.summoner.puuid == player_id:
                self = team_member
                win = player_game.win

        assert self is not None, "Own player not appeared in games"
        ret_games.append(
            Game(
                match_id=game.match_id,
                victorious_team=TeamSide.red
                if self.team == TeamSide.red and win
                else TeamSide.blue,
                ally_team=ally_team,
                enemy_team=enemy_team,
                duration=game.duration,
                timestamp=db_to_datetime(game.start_time),
                self=self,
                win=win,
            )
        )
    return Page[Game](items=ret_games, next=str(next_link))
