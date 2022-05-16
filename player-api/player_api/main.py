import json
import string
import random
import time
from urllib.parse import urlencode
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Depends
from sqlalchemy import func, text, case, desc
import logging.config
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from sqlalchemy.orm import Session

from player_api.models.game import (
    Game,
    Page,
    TeamSide,
    TeamMember,
    Champion,
    GamePlayer,
    NameValue,
)
from player_api.db import Summoners, Games, Champions, SessionLocal
from player_api.models.player import Player, Rank, MostPlayed, BasicPlayer
from player_api.models.responses import ExceptionMessage

logging.config.fileConfig(
    Path(__file__).parent.joinpath("logging.conf"), disable_existing_loggers=False
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Player API",
    version="1.0.0",
    servers=[{"url": "https://lol-stats.de/api"}],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


PlayerId = str
PlayerName = str

DEFAULT_GAMES_PER_PAGE = 5


@app.middleware("http")
async def log_requests(request: Request, call_next):
    rid = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"{rid=} path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"{rid=} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


@app.get(
    "/players/{player_id}",
    response_model=Player,
    responses={404: {"model": ExceptionMessage, "description": "Player not found"}},
)
async def get_player(player_id: PlayerId, db: Session = Depends(get_db)):
    """Get a player by riots puuid"""
    logger.debug(f"method=get_player {player_id=}")
    player = get_player_by_id(db, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="player not found")
    logger.debug(f"method=get_player {player_id=} {player.name=}")

    most_played_db = (
        db.query(
            Games.champ_id,
            Champions.name,
            Champions.icon_path,
            func.count(Games.champ_id).label("num_played"),
            func.count(case([(Games.win, 1)])).label("won"),
        )
        .join(Champions)
        .where(Games.summoner_id == player.puuid)
        .group_by(Games.champ_id, Champions.name, Champions.icon_path)
        .order_by(text("num_played DESC"))
        .limit(5)
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
    logging.debug(f"method=get_player {most_played=}")

    result = (
        db.query(
            func.count(Games.summoner_id).label("num_played"),
            func.count(case([(Games.win, 1)])).label("won"),
        )
        .where(Games.summoner_id == player.puuid)
        .first()
    )
    win_rate = calc_win_rate(result.num_played, result.won)
    logging.debug(f"method=get_player {win_rate=}")
    return Player(
        id=player.puuid,
        player_icon_path=player.icon_path,
        name=player.name,
        level=player.level,
        rank=Rank(
            division=Rank.division_from_str(player.division), tier=player.tier, league_points=player.league_points
        ),
        most_played=most_played,
        win_rate=win_rate,
    )


@app.get(
    "/players",
    response_model=BasicPlayer,
    responses={404: {"model": ExceptionMessage, "description": "Player not found"}},
)
def find_player(player_name: str, region: str = None, db: Session = Depends(get_db)):
    player = get_player_by_name(db, player_name)
    if player is None:
        raise HTTPException(status_code=404, detail="player not found")
    return BasicPlayer(
        id=player.puuid,
        player_icon_path=player.icon_path,
        name=player.name,
        level=player.level,
        rank=Rank(
            division=Rank.division_from_str(player.division), tier=player.tier, league_points=player.league_points
        ),
    )


def get_player_by_id(db: Session, player_id: str) -> Summoners | None:
    player: Summoners | None = (
        db.query(Summoners).where(Summoners.puuid == player_id).first()
    )
    return player


@app.get(
    "/players/{player_name}/recent-games",
    response_model=Page[Game],
    responses={404: {"model": ExceptionMessage, "description": "Player not found"}},
)
def recent_games(
    player_name: PlayerName,
    request: Request,
    start_after: datetime = None,
    limit: int = DEFAULT_GAMES_PER_PAGE,
    db: Session = Depends(get_db)
):
    logger.debug(f"method=recent_games {player_name=}")
    player = get_player_by_name(db, player_name)
    if player is None:
        raise HTTPException(status_code=404, detail="player not found")
    logger.debug(f"method=recent_games {player_name=} {player.puuid=}")
    if start_after is None:
        start_after = datetime(1970, 1, 1)
    games: list[Games] = (
        db.query(Games)
        .where(Summoners.puuid == player.puuid and Games.start_time > start_after)
        .order_by(desc(Games.start_time))
        .limit(limit)
        .all()
    )
    if len(games) == 0:
        return Page[Game](items=[], next="")
    next_start_after = games[0].start_time.isoformat()
    next_link = (
        str(request.url.path)
        + "?"
        + urlencode({"start_after": next_start_after, "limit": limit})
    )
    ret_games = []
    for game in games:
        stats = [NameValue(name=k, value=v) for k, v in json.loads(game.stats).items()]
        ret_games.append(
            Game(
                match_id=game.match_id,
                victorious_team=TeamSide.red,
                ally_team=[
                    TeamMember(
                        champion=Champion(
                            name=game.champion.name, icon_path=game.champion.icon_path
                        ),
                        player=GamePlayer(id=player.puuid, name=player.name),
                        player_stats=stats,
                    )
                ],
                enemy_team=[],
                duration=game.duration,
                timestamp=game.start_time,
            )
        )
    return Page[Game](items=ret_games, next=str(next_link))


def get_player_by_name(db: Session, player_name: str) -> Summoners | None:
    player: Summoners | None = (
        db.query(Summoners).where(Summoners.name == player_name).first()
    )
    return player


def calc_win_rate(games: int, won: int) -> int:
    if won == 0:
        return 0
    if won > games:
        raise ValueError(f"Won more games than played. {games=} {won=}")
    return int((won / games) * 100)


FastAPIInstrumentor.instrument_app(app)
