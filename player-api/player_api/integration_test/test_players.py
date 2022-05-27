import random

from fastapi.testclient import TestClient

from integration_test.test_main import PlayerFactory, Testplayer
from main import app
from models.player import BasicPlayer

client = TestClient(app)
random.seed(1)


def test_find_player(db_session):
    players = PlayerFactory(db_session).player()
    with players:
        pass
    res = _player_reqeust_by_name(players[0].name)
    assert res is not None
    assert res.id == players[0].player.id
    assert res.name == players[0].player.name
    assert res.imported is True


def test_find_player_not_exist(db_session):
    players = PlayerFactory(db_session).player()
    with players:
        pass
    res = _player_reqeust_by_name("NON_EXISTENT")
    assert res is None


def test_find_player_riot_api_only(db_session, requests_mock):
    requests_mock.real_http = True
    player_name = "RIOT_ONLY"
    player_id = "THIS_IS_A_RANDOM_ID"
    requests_mock.get(
        f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player_name}",
        json={"name": player_name, "puuid": player_id, "summonerLevel": 1},
    )
    player_exists_in_riot_api(player_name, player_id)
    res = _player_reqeust_by_name(player_name)
    assert res is not None
    assert res.name == player_name
    assert res.id == player_id
    assert res.imported is False


def _player_reqeust_by_name(name: str) -> BasicPlayer | None:
    response = client.get(f"/players?player_name={name}")
    if response.status_code == 200:
        return BasicPlayer(**response.json())
    else:
        return None


def player_exists_in_riot_api(player_name: str, player_id: str):
    pass
