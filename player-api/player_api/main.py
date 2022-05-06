import os

from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import func, text, case

from player_api.db import Summoners, Games
from player_api.models.factories import PlayerModelFactory
from player_api.models.player import Player, Rank, MostPlayed
from player_api.models.responses import ExceptionMessage

app = FastAPI(
    title="Player API",
    version="1.0.0",
    servers=[{"url": "https://lol-stats.de/api", "name": "production"}],
)
app.add_middleware(
    DBSessionMiddleware,
    db_url=f"postgresql://postgres:{os.environ.get('POSTGRES_PASSWORD', 'postgres')}@"
    f"{os.environ.get('POSTGRES_HOST', 'localhost')}/postgres",
)

PlayerId = str
PlayerName = str


@app.get(
    "/players/{player_name}",
    response_model=Player,
    responses={404: {"model": ExceptionMessage, "description": "Player not found"}},
)
async def get_player(player_name: PlayerName):
    """Get a player by player name"""
    player_id = get_player_id(player_name)
    if player_id is None:
        raise HTTPException(status_code=404, detail="player not found")

    players: list[Summoners] = (
        db.session.query(Summoners).where(Summoners.puuid == player_id).all()
    )
    player = players[0]
    most_played_db = (
        db.session.query(
            Games.champion_id,
            func.count(Games.champion_id).label("num_played"),
            func.count(case([(Games.win, 1)])).label("won"),
        )
        .where(Games.summoner_id == player_id)
        .group_by(Games.champion_id)
        .order_by(text("num_played DESC"))
        .limit(5)
        .all()
    )
    most_played = []
    for champ in most_played_db:
        most_played.append(
            MostPlayed(
                champion_id=champ[0],
                games=champ[1],
                win_rate=calc_win_rate(games=champ[1], won=champ[2]),
            )
        )

    win_rate = 0  # TODO
    return Player(
        id=player_id,
        icon_path=player.icon_path,
        name=player.name,
        level=player.level,
        rank=Rank(
            rank=player.rank, tier=player.tier, league_points=player.league_points
        ),
        most_played=most_played,
        win_rate=win_rate,
    )


def get_player_id(player_name: str) -> str | None:
    with db():
        players: list[Summoners] = (
            db.session.query(Summoners).where(Summoners.name == player_name).all()
        )
        if not players:
            return None
        else:
            assert (
                len(players) == 1
            ), f"Player ID should be unique. Got {len(players)} players"
            return players[0].puuid


def calc_win_rate(games: int, won: int) -> int:
    if won == 0:
        return 0
    if won > games:
        raise ValueError(f"Won more games than played. {games=} {won=}")
    return int((won / games) * 100)
