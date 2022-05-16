import random

import pytest
from fastapi.testclient import TestClient

from integration_test.factories import PlayerFactory, Testplayer, Champion
from player_api.main import app, calc_win_rate
from player_api.models.player import Player

client = TestClient(app)
random.seed(1)


def test_get_most_played(db_session):
    players = PlayerFactory(db_session).player()
    player = players[0]
    with players:
        player.play_n_games(10).with_champion("Lux").win(4)
        player.play_n_games(5).with_champion("Azir").win(5)
        player.play_n_games(4).with_champion("Annie").win(0)
        player.play_n_games(3).with_champion("Thresh").win(0)
    res = _player_reqeust(player)
    assert res.most_played[0].champion_id == Champion(db_session, "Lux").id
    assert res.most_played[0].games == 10
    assert res.most_played[0].win_rate == calc_win_rate(10, 4)
    assert res.most_played[1].champion_id == Champion(db_session, "Azir").id
    assert res.most_played[1].games == 5
    assert res.most_played[1].win_rate == calc_win_rate(5, 5)
    assert res.most_played[2].champion_id == Champion(db_session, "Annie").id
    assert res.most_played[2].games == 4
    assert res.most_played[2].win_rate == calc_win_rate(4, 0)
    assert res.most_played[3].champion_id == Champion(db_session, "Thresh").id
    assert res.most_played[3].games == 3
    assert res.most_played[3].win_rate == calc_win_rate(3, 0)


def test_no_games_played(db_session):
    players = PlayerFactory(db_session).player()
    player = players[0]
    with players:
        pass
    res = _player_reqeust(player)
    assert res.most_played == []


def test_get_most_played_champ_name(db_session):
    players = PlayerFactory(db_session).player()
    player = players[0]
    with players:
        player.play_n_games(30).with_champion("Lux").win(4)
    res = _player_reqeust(player)
    assert len(res.most_played) == 1
    assert res.most_played[0].champion_name == "Lux"


def test_get_most_played_many_champs(db_session):
    players = PlayerFactory(db_session).player()
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
    assert res.most_played[0].champion_id == Champion(db_session, "Lux").id
    assert res.most_played[1].champion_id == Champion(db_session, "Azir").id
    assert res.most_played[2].champion_id == Champion(db_session, "Annie").id
    assert res.most_played[3].champion_id == Champion(db_session, "Thresh").id
    assert res.most_played[4].champion_id == Champion(db_session, "Aatrox").id


@pytest.mark.skip
def test_performance(db_session, benchmark):
    players = PlayerFactory(db_session).n_players(5000)
    with players:
        for player in players:
            player.play_n_games(100).with_champion("Lux").win(44)
            player.play_n_games(50).with_champion("Azir").win(30)
            player.play_n_games(3).with_champion("Braum").win(1)
    _player_reqeust(players[0])


def test_win_rate(db_session):
    players = PlayerFactory(db_session).player()
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
