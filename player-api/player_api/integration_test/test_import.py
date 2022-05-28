from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from player_api.import_state import global_import_state
from player_api.models.player import (
    ImportProgress,
    Player,
    BasicPlayer,
    ImportState,
    PlayerId,
    PlayerName,
)
from player_api.main import app

client = TestClient(app)

PLAYER_NAME = "TEST_PLAYER"
PLAYER_ID = "TEST_UUID"
REGION = "euw1"


@pytest.fixture
def clean_global_state():
    global_import_state.players = {}


def test_import_state(requests_mock, clean_global_state):
    requests_mock.real_http = True
    requests_mock.get(
        f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{PLAYER_NAME}",
        json={"name": PLAYER_NAME, "puuid": PLAYER_ID, "summonerLevel": 1},
    )
    requests_mock.get(
        f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{PLAYER_ID}",
        json={"name": PLAYER_NAME, "puuid": PLAYER_ID, "summonerLevel": 1},
    )
    res = import_player(PLAYER_ID)
    assert res.imported is False

    res = get_player(PLAYER_ID)
    assert res.imported is False
    res = find_player(PLAYER_NAME)
    assert res.imported is False

    global_import_state.set_import_state(
        player_id=PLAYER_ID,
        progress=ImportProgress(
            imported_games=5,
            total_games=5,
            import_state=ImportState.FINISHED,
            imported=True,
            percentage=ImportProgress.calc_percentage(5, 5),
        ),
    )

    res = import_player(PLAYER_ID)
    assert res.imported is True

    res = find_player(PLAYER_NAME)
    assert res.imported is True


def test_import_multiple_times(clean_global_state):
    res = import_player(PLAYER_ID)
    assert res.imported is False
    res = import_player(PLAYER_ID)
    assert res.imported is False

    global_import_state.set_import_state(
        player_id=PLAYER_ID,
        progress=ImportProgress(
            imported_games=5,
            total_games=5,
            import_state=ImportState.FINISHED,
            imported=True,
            percentage=ImportProgress.calc_percentage(5, 5),
        ),
    )

    res = import_player(PLAYER_ID)
    assert res.imported is True
    res = import_player(PLAYER_ID)
    assert res.imported is True


def import_player(player_id: PlayerId) -> ImportProgress:
    res = client.post(f"/players/{player_id}/import")
    assert res.ok
    return ImportProgress(**res.json())


def get_player(player_id: PlayerId) -> Player:
    res = client.get(f"/players/{player_id}")
    assert res.ok
    return Player(**res.json())


def find_player(player_name: PlayerName) -> BasicPlayer:
    res = client.get(f"/players?player_name={player_name}")
    assert res.ok
    return BasicPlayer(**res.json())
