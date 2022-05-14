from fastapi.testclient import TestClient
from player_api.main import app
from player_api.models.player import Player

client = TestClient(app)


def test_get_valid_player():
    response = client.get("/players/1")
    assert response.status_code == 200
    assert Player(**response.json())
