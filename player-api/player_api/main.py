import os

from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import func

from player_api.db import Summoners, Games
from player_api.models.factories import PlayerFactory
from player_api.models.player import Player
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


@app.get(
    "/players/{player}",
    response_model=Player,
    responses={404: {"model": ExceptionMessage, "description": "Player not found"}},
)
async def get_player(player: PlayerId):
    player_id = player
    players: list[Summoners] = (
        db.session.query(Summoners).where(Summoners.puuid == player_id).all()
    )

    if not players:
        raise HTTPException(status_code=404, detail="player not found")
    assert len(players) == 1, f"Player ID should be unique. Got {len(players)} players"
    player = players[0]
    most_played = (
        db.session.query(
            Games.champion_id, func.count(Games.champion_id).label("num_played")
        )
        .where(Games.summoner_id == player_id)
        .group_by(Games.champion_id)
        .order_by("num_played DESC")
        .limit(5)
        .all()
    )
    print(most_played)
    return PlayerFactory.build(id=player_id, icon_path=player.icon_path)
