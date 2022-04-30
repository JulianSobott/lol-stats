from pydantic_factories import ModelFactory, Use
import random

from player_api.models.player import Player, Rank, RankEnum, TierEnum, MostPlayed


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
