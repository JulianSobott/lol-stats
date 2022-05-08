import os
import string
import random
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import func, text, case
import logging.config
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


from player_api.db import Summoners, Games, Champions
from player_api.models.player import Player, Rank, MostPlayed
from player_api.models.responses import ExceptionMessage

logging.config.fileConfig(Path(__file__).parent.joinpath("logging.conf"), disable_existing_loggers=False)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Player API",
    version="1.0.0",
    servers=[{"url": "https://lol-stats.de/api"}],
)
app.add_middleware(
    DBSessionMiddleware,
    db_url=f"postgresql://postgres:{os.environ.get('POSTGRES_PASSWORD', 'postgres')}@"
    f"{os.environ.get('POSTGRES_HOST', 'localhost')}/postgres",
)

PlayerId = str
PlayerName = str


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
    "/players/{player_name}",
    response_model=Player,
    responses={404: {"model": ExceptionMessage, "description": "Player not found"}},
)
async def get_player(player_name: PlayerName):
    """Get a player by player name"""
    logger.debug(f"method=get_player {player_name=}")
    player = get_player_by_name(player_name)
    if player is None:
        raise HTTPException(status_code=404, detail="player not found")
    logger.debug(f"method=get_player {player_name=} {player.puuid=}")

    most_played_db = (
        db.session.query(
            Games.champ_id,
            Champions.name,
            Champions.icon_path,
            func.count(Games.champ_id).label("num_played"),
            func.count(case([(Games.win, 1)])).label("won"),
        )
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
        db.session.query(
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
            rank=player.rank, tier=player.tier, league_points=player.league_points
        ),
        most_played=most_played,
        win_rate=win_rate,
    )


def get_player_by_name(player_name: str) -> Summoners | None:
    with db():
        player: Summoners | None = (
            db.session.query(Summoners).where(Summoners.name == player_name).first()
        )
        return player


def calc_win_rate(games: int, won: int) -> int:
    if won == 0:
        return 0
    if won > games:
        raise ValueError(f"Won more games than played. {games=} {won=}")
    return int((won / games) * 100)


FastAPIInstrumentor.instrument_app(app)
