import json
import os

from fastapi import FastAPI
from redis import Redis
from player_api.models.player import Player, Rank, MostPlayed, RankEnum, TierEnum

app = FastAPI()
redis = Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379, db=0)

PlayerId = int


@app.get("/players/{player}", response_model=Player)
async def get_player(player: PlayerId):
    player_id = player
    res = redis.get(f"player:{player_id}")
    if res:
        print("taken from cache")
        return Player(**json.loads(res))
    else:
        player = fetch_player(player_id)
        cache_player_data(player_id, player)
        return player


def fetch_player(player_id: PlayerId) -> Player:
    # TODO: fetch from Riot API
    from pydantic_factories import ModelFactory, Use
    import random

    class PlayerFactory(ModelFactory):
        __model__ = Player

        win_rate = Use(random.randint, 0, 100)
        rank = Use(lambda: RankFactory.build())
        most_played = Use(lambda: MostPlayedFactory.batch(5))

    class RankFactory(ModelFactory):
        __model__ = Rank

        rank = Use(random.choice, list(RankEnum))
        tier = Use(random.choice, list(TierEnum))
        league_points = Use(random.randint, 0, 100)

    class MostPlayedFactory(ModelFactory):
        __model__ = MostPlayed

        champion_id = Use(random.randint, 0, 200)
        rank = Use(random.randint, 0, 100)

    return PlayerFactory.build(id=player_id)


def cache_player_data(player_id: PlayerId, player: Player):
    encoded = player.json()
    redis.set(f"player:{player_id}", encoded)
