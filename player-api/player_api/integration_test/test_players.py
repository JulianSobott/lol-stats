import random

from fastapi.testclient import TestClient

from player_api.db import Summoners
from player_api.integration_test.factories import PlayerFactory
from player_api.main import app
from player_api.models.player import BasicPlayer, TierEnum

client = TestClient(app)
random.seed(1)

PLAYER_ID = "TEST_PUUID"


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


def test_get_incomplete_db_player(db_session):
    player = Summoners(puuid=PLAYER_ID, region_id=PLAYER_ID, name="xyz", level=1)
    db_session.add(player)
    db_session.commit()
    response_player = _player_reqeust_by_name("xyz")
    assert response_player.id == PLAYER_ID
    assert response_player.imported is False


def test_get_unranked(db_session):
    player = Summoners(
        puuid=PLAYER_ID,
        region_id=PLAYER_ID,
        name="xyz",
        level=1,
        tier=TierEnum.UNRANKED,
        last_update=16000,
        icon_path="test.png",
    )
    db_session.add(player)
    db_session.commit()
    response_player = _player_reqeust_by_name("xyz")
    assert response_player.id == PLAYER_ID
    assert response_player.imported is True


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
