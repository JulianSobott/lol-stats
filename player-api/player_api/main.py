import os

from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db

from player_api.db import Summoners
from player_api.models.factories import PlayerFactory
from player_api.models.player import Player

app = FastAPI()
app.add_middleware(DBSessionMiddleware,
                   db_url=f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@"
                          f"{os.environ['POSTGRES_HOST']}/postgres")


PlayerId = str


@app.get("/players/{player}", response_model=Player)
async def get_player(player: PlayerId):
    player_id = player
    players: list[Summoners] = db.session.query(Summoners).where(Summoners.puuid == player_id).all()
    if not players:
        raise HTTPException(status_code=404, detail="Player not found")
    assert len(players) == 1, f"Player ID should be unique. Got {len(players)} players"
    player = players[0]
    # TODO: fetch all from Database
    return PlayerFactory.build(id=player_id, icon_path=player.icon_path)
