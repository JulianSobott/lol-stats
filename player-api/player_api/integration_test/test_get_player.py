from fastapi.testclient import TestClient

from player_api.db import Summoners
from player_api.main import app
from player_api.models.player import Player, PlayerId, TierEnum, Rank

PLAYER_ID = "TEST_PUUID"

client = TestClient(app)


def test_get_incomplete_db_player(db_session, requests_mock):
    requests_mock.real_http = True
    requests_mock.get(
        f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{PLAYER_ID}",
        json={"name": "xyz", "puuid": PLAYER_ID, "summonerLevel": 1},
    )

    player = Summoners(puuid=PLAYER_ID, region_id=PLAYER_ID, name="xyz", level=1)
    db_session.add(player)
    db_session.commit()
    response_player = _player_reqeust(PLAYER_ID)
    assert response_player.id == PLAYER_ID
    assert response_player.imported is False


def test_get_unranked_player(db_session):
    player = Summoners(
        puuid=PLAYER_ID,
        region_id=PLAYER_ID,
        name="xyz",
        level=1,
        icon_path="/icon.png",
        last_update=160000,
        tier=TierEnum.UNRANKED,
        division=None,
        league_points=None,
    )
    db_session.add(player)
    db_session.commit()
    response_player = _player_reqeust(PLAYER_ID)
    assert response_player.id == PLAYER_ID
    assert response_player.imported is True
    assert response_player.rank == Rank(
        division=1, tier=TierEnum.UNRANKED, league_points=0
    )


def _player_reqeust(player_id: PlayerId) -> Player:
    response = client.get(f"/players/{player_id}")
    assert response.status_code == 200
    return Player(**response.json())
