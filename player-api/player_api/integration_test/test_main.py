import string
import random
from datetime import datetime, timedelta

import pytest
from pytest import fixture
from fastapi.testclient import TestClient
from requests import Session
from sqlalchemy import create_engine

from fastapi_sqlalchemy import db

from player_api.db import Champions, Summoners, Base, Games
from player_api.main import app, calc_win_rate
from player_api.models.factories import PlayerModelFactory
from player_api.models.player import Player

client = TestClient(app)
random.seed(1)


def test_get_most_played(db_session):
    players = PlayerFactory().player()
    player = players[0]
    with players:
        player.play_n_games(10).with_champion("Lux").win(4)
        player.play_n_games(5).with_champion("Azir").win(5)
        player.play_n_games(4).with_champion("Annie").win(0)
        player.play_n_games(3).with_champion("Thresh").win(0)
    res = _player_reqeust(player)
    assert res.most_played[0].champion_id == Champion("Lux").id
    assert res.most_played[0].games == 10
    assert res.most_played[0].win_rate == calc_win_rate(10, 4)
    assert res.most_played[1].champion_id == Champion("Azir").id
    assert res.most_played[1].games == 5
    assert res.most_played[1].win_rate == calc_win_rate(5, 5)
    assert res.most_played[2].champion_id == Champion("Annie").id
    assert res.most_played[2].games == 4
    assert res.most_played[2].win_rate == calc_win_rate(4, 0)
    assert res.most_played[3].champion_id == Champion("Thresh").id
    assert res.most_played[3].games == 3
    assert res.most_played[3].win_rate == calc_win_rate(3, 0)


def test_no_games_played(db_session):
    players = PlayerFactory().player()
    player = players[0]
    with players:
        pass
    res = _player_reqeust(player)
    assert res.most_played == []


def test_get_most_played_champ_name(db_session):
    players = PlayerFactory().player()
    player = players[0]
    with players:
        player.play_n_games(30).with_champion("Lux").win(4)
    res = _player_reqeust(player)
    assert len(res.most_played) == 1
    assert res.most_played[0].champion_name == "Lux"


def test_get_most_played_many_champs(db_session):
    players = PlayerFactory().player()
    player = players[0]
    with players:
        player.play_n_games(30).with_champion("Lux").win(4)
        player.play_n_games(20).with_champion("Azir").win(5)
        player.play_n_games(11).with_champion("Annie").win(11)
        player.play_n_games(10).with_champion("Thresh").win(1)
        player.play_n_games(9).with_champion("Aatrox").win(1)
        player.play_n_games(8).with_champion("Quinn").win(1)
        player.play_n_games(7).with_champion("Braum").win(1)
    res = _player_reqeust(player)
    assert len(res.most_played) == 5
    assert res.most_played[0].champion_id == Champion("Lux").id
    assert res.most_played[1].champion_id == Champion("Azir").id
    assert res.most_played[2].champion_id == Champion("Annie").id
    assert res.most_played[3].champion_id == Champion("Thresh").id
    assert res.most_played[4].champion_id == Champion("Aatrox").id


@pytest.mark.skip
def test_performance(db_session, benchmark):
    players = PlayerFactory().n_players(5000)
    with players:
        for player in players:
            player.play_n_games(100).with_champion("Lux").win(44)
            player.play_n_games(50).with_champion("Azir").win(30)
            player.play_n_games(3).with_champion("Braum").win(1)
    _player_reqeust(players[0])


def test_win_rate(db_session):
    players = PlayerFactory().player()
    player = players[0]
    with players:
        player.play_n_games(10).win(5)
        player.play_n_games(10).win(5)
    res = _player_reqeust(player)
    assert res.win_rate == 50


def _player_reqeust(player: "Testplayer") -> Player:
    response = client.get(f"/players/{player.player.id}")
    assert response.status_code == 200
    return Player(**response.json())


class PlayerFactory:
    def __init__(self):
        self.players: list["Testplayer"] = []

    def player(self) -> "PlayerFactory":
        self.players.append(Testplayer())
        return self

    def n_players(self, num_players: int) -> "PlayerFactory":
        self.players.extend(Testplayer() for i in range(num_players))
        return self

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        with db():
            objects = []
            for player in self.players:
                objects.append(player.summoner)
                for game in player.games:
                    objects.append(game)
            db.session.bulk_save_objects(objects)
            db.session.commit()

    def __getitem__(self, item):
        return self.players[item]

    def __iter__(self):
        for player in self.players:
            yield player


class Testplayer:
    def __init__(self, **kwargs):
        self.player: Player = PlayerModelFactory.build(**kwargs)
        self.games_factories: list[GamesFactory] = []

    def play_n_games(self, num_games: int) -> "GamesFactory":
        factory = GamesFactory(self).with_n_games(num_games)
        self.games_factories.append(factory)
        return factory

    @property
    def summoner(self):
        return Summoners(
            puuid=self.player.id,
            name=self.player.name,
            level=self.player.level,
            icon_path=self.player.player_icon_path,
            last_update=datetime.now(),
            tier=self.player.rank.tier,
            rank=self.player.rank.rank,
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


class GamesFactory:
    def __init__(self, player: Testplayer):
        self.num_games = 0
        self.champion = "Aatrox"
        self.won = 0
        self.player = player

    def with_n_games(self, num_games: int) -> "GamesFactory":
        self.num_games = num_games
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

        for i in range(self.num_games):
            if available_won == 0:
                won = False
            else:
                won = True
                available_won -= 1
            objects.append(
                Games(
                    match_id=random_name(),
                    summoner_id=self.player.summoner.puuid,
                    champ_id=Champion(self.champion).id,
                    start_time=datetime.now() - timedelta(hours=1),
                    duration=timedelta(minutes=30).total_seconds(),
                    win=won,
                    lane="bottom",
                    stats="",
                    challenges="",
                )
            )
        return objects


class Champion:
    cache = {}

    def __new__(cls, name, *args, **kwargs) -> Champions:
        if name in Champion.cache:
            return Champion.cache[name]
        # DB read not possible, because we clean database before each test
        with db():
            champ = Champions(
                id=len(Champion.cache),
                name=name,
                icon_path=f"https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/{name}.png",
            )
            db.session.bulk_save_objects([champ])
            db.session.commit()
            # champ = db.session.query(Champions).where(Champions.name == name).all()[0]
        Champion.cache[name] = champ
        return Champion.cache[name]


def random_name():
    return "".join(
        random.choice(string.ascii_letters) for _ in range(random.randint(5, 10))
    )
