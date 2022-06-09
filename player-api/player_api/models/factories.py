from pydantic_factories import ModelFactory, Use
import random

from player_api.models.player import Player, Rank, TierEnum, MostPlayed


class PlayerModelFactory(ModelFactory):
    __model__ = Player

    win_rate = Use(random.randint, 0, 100)
    rank = Use(lambda: RankModelFactory.build())
    most_played = Use(lambda: MostPlayedModelFactory.batch(5))


class RankModelFactory(ModelFactory):
    __model__ = Rank

    rank = Use(random.randint, 1, 4)
    tier = Use(random.choice, list(TierEnum))
    league_points = Use(random.randint, 0, 100)


class MostPlayedModelFactory(ModelFactory):
    __model__ = MostPlayed

    champion_id = Use(random.randint, 0, 200)
    rank = Use(random.randint, 0, 100)
