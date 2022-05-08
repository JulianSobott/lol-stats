import random

from fastapi.testclient import TestClient

from integration_test.test_main import PlayerFactory, Testplayer
from main import app
from models.player import BasicPlayer

client = TestClient(app)
random.seed(1)


def test_find_player(db_session):
    players = PlayerFactory().player()
    with players:
        pass
    res = _player_reqeust_by_name(players[0].name)
    assert res is not None
    assert res.id == players[0].player.id
    assert res.name == players[0].player.name


def test_find_player_not_exist(db_session):
    players = PlayerFactory().player()
    with players:
        pass
    res = _player_reqeust_by_name("NON_EXISTENT")
    assert res is None


def _player_reqeust_by_name(name: str) -> BasicPlayer | None:
    response = client.get(f"/players?player_name={name}")
    if response.status_code == 200:
        return BasicPlayer(**response.json())
    else:
        return None
