import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from player_api.db import ChallengeClasses
from player_api.integration_test.factories import PlayerFactory
from player_api.main import app
from player_api.models.leaderboards import Leaderboards, Challenge, LeaderboardPlayer

client = TestClient(app)


challenges = [f"challenge_{i}" for i in range(1)]
categories = [f"category_{i}" for i in range(2)]
puuids = [f"player_{i}" for i in range(5)]


@pytest.fixture
def setup_challenges(db_session: Session):
    objects = [
        ChallengeClasses(
            name=challenge,
            class_name=categories[0],
            comparison_operator=">",
            description=challenge,
        )
        for challenge in challenges[:3]
    ]
    db_session.bulk_save_objects(objects)
    db_session.commit()


def test_leaderboards(db_session: Session, setup_challenges):
    players = PlayerFactory(db_session).n_players(3)
    players[0].player.id = puuids[0]
    players[1].player.id = puuids[1]
    players[2].player.id = puuids[2]
    with players:
        players[0].add_challenge(name=challenges[0], highscore=1, total=1, avg=10)
        players[1].add_challenge(name=challenges[0], highscore=1, total=1, avg=5)
        players[2].add_challenge(name=challenges[0], highscore=1, total=1, avg=2)
    leaderboards = _leaderboards_request(num_challenges=1, num_players=2)
    assert len(leaderboards.challenges) == 1

    assert leaderboards.challenges[0].players[0].id == puuids[0]
    assert leaderboards.challenges[0].players[1].id == puuids[1]

    assert leaderboards.challenges[0].players[0].value == 10
    assert leaderboards.challenges[0].players[1].value == 5


def _leaderboards_request(num_challenges: int, num_players: int):
    response = client.get(
        f"/achievements/leaderboards?challenges={num_challenges}&players={num_players}"
    )
    assert response.status_code == 200
    return Leaderboards(**response.json())
