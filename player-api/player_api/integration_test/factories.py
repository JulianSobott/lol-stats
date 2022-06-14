import json
import random
import string
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from player_api.models.player import Player, TierEnum
from player_api.db import Champions, Summoners, Base, Games, datetime_to_db, Challenges
from player_api.models.factories import PlayerModelFactory

DEFAULT_GAME_LENGTH = 30


class PlayerFactory:
    def __init__(self, db: Session):
        self.db = db
        self.players: list["Testplayer"] = []

    def player(self) -> "PlayerFactory":
        self.players.append(Testplayer(self.db))
        return self

    def n_players(self, num_players: int) -> "PlayerFactory":
        self.players.extend(Testplayer(self.db) for i in range(num_players))
        return self

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        objects = []
        for player in self.players:
            objects.append(player.summoner)
            objects.extend(player.games)
            objects.extend(player.challenges)
        self.db.bulk_save_objects(objects)
        self.db.commit()

    def __getitem__(self, item):
        return self.players[item]

    def __iter__(self):
        for player in self.players:
            yield player


class Testplayer:
    def __init__(self, db: Session, **kwargs):
        self.db = db
        self.player: Player = PlayerModelFactory.build(**kwargs)
        self.games_factories: list[GamesFactory] = []
        self.elo = TierEnum.CHALLENGER
        self._challenges = []

    def play_n_games(self, num_games: int) -> "GamesFactory":
        factory = GamesFactory(self.db, self).with_n_games(num_games)
        self.games_factories.append(factory)
        return factory

    def with_elo(self, elo: TierEnum):
        self.elo = elo
        return self

    def add_challenge(self, name: str, highscore: float, total: float, avg: float):
        challenge = Challenges(
            name=name,
            summoner_id=self.player.id,
            total=total,
            average_per_game=avg,
            highscore=highscore,
        )
        self._challenges.append(challenge)
        return self

    @property
    def summoner(self):
        return Summoners(
            puuid=self.player.id,
            name=self.player.name,
            level=self.player.level,
            icon_path=self.player.player_icon_path,
            last_update=datetime_to_db(datetime.now()),
            tier=self.elo,
            division=self.player.rank.division_str,
            league_points=self.player.rank.league_points,
        )

    @property
    def name(self):
        return self.player.name

    @property
    def games(self):
        objects = []
        for factory in self.games_factories:
            objects.extend(factory.games)
        return objects

    @property
    def challenges(self):
        return self._challenges


class GamesFactory:
    def __init__(self, db: Session, player: Testplayer):
        self.db = db
        self.num_games = 0
        self.champion = "Aatrox"
        self.won = 0
        self.player = player
        self.start = datetime.now() - timedelta(days=7)

    def with_n_games(self, num_games: int) -> "GamesFactory":
        self.num_games = num_games
        return self

    def starting_at(self, start: datetime) -> "GamesFactory":
        self.start = start
        return self

    def with_champion(self, champion: str) -> "GamesFactory":
        self.champion = champion
        return self

    def win(self, num_games: int):
        if num_games > self.num_games:
            raise ValueError(
                f"Won more games than played. {self.num_games=} won={num_games}"
            )
        self.won = num_games
        return self

    @property
    def games(self):
        objects = []
        available_won = self.won
        with open("example_stats.json") as f:
            stats = f.read()
        for i in range(self.num_games):
            if available_won == 0:
                won = False
            else:
                won = True
                available_won -= 1
            match_id = random_name()
            objects.append(
                Games(
                    match_id=match_id,
                    summoner_id=self.player.summoner.puuid,
                    champ_id=Champion(self.db, self.champion).id,
                    start_time=datetime_to_db(
                        self.start + timedelta(minutes=i * DEFAULT_GAME_LENGTH)
                    ),
                    duration=int(
                        timedelta(minutes=DEFAULT_GAME_LENGTH).total_seconds()
                    ),
                    win=won,
                    lane="bottom",
                    team="red",
                    challenges=stats,
                )
            )
            for j in range(9):
                summoner = Testplayer(self.db).summoner
                self.db.add(summoner)
                self.db.commit()
                objects.append(
                    Games(
                        match_id=match_id,
                        summoner_id=summoner.puuid,
                        champ_id=Champion(self.db, self.champion).id,
                        start_time=datetime_to_db(
                            self.start + timedelta(minutes=i * DEFAULT_GAME_LENGTH)
                        ),
                        duration=int(
                            timedelta(minutes=DEFAULT_GAME_LENGTH).total_seconds()
                        ),
                        win=won if j < 4 else not won,
                        lane="bottom",
                        team="red" if j < 4 else "blue",
                        challenges=stats,
                    )
                )
        return objects


class Champion:
    def __new__(cls, db: Session, name, *args, **kwargs) -> Champions:
        res = db.query(Champions).where(Champions.name == name).all()
        if res:
            return res[0]

        champ = Champions(
            id=random.randint(0, 50000),
            name=name,
            icon_path=f"https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/{name}.png",
        )
        db.add(champ)
        db.commit()
        db.refresh(champ)
        # champ = db.session.query(Champions).where(Champions.name == name).all()[0]
        return champ


def random_name():
    return "".join(
        random.choice(string.ascii_letters) for _ in range(random.randint(5, 10))
    )
