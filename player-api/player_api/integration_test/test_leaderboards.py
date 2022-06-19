import random

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from player_api.db import ChallengeClasses
from player_api.integration_test.factories import PlayerFactory
from player_api.main import app
from player_api.models.leaderboards import Leaderboards

client = TestClient(app)


challenges = [f"challenge_{i}" for i in range(10)]
categories = [f"category_{i}" for i in range(5)]
puuids = [f"player_{i}" for i in range(10)]

random.seed(1)


def setup_challenges(
    db_session: Session, *, num_challenges_per_cat: int, num_categories: int
):
    objects = []
    for i, category in enumerate(categories[:num_categories]):
        for challenge in challenges[
            num_challenges_per_cat * i : num_challenges_per_cat * (i + 1)
        ]:
            objects.append(
                ChallengeClasses(
                    name=challenge,
                    class_name=category,
                    comparison_operator=">" if i % 2 == 0 else "<",
                    description=challenge,
                )
            )
    db_session.bulk_save_objects(objects)
    db_session.commit()


def test_leaderboards_sorting(db_session: Session):
    setup_challenges(db_session, num_categories=1, num_challenges_per_cat=1)
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


def test_leaderboards_random_challenges(db_session: Session):
    setup_challenges(db_session, num_categories=1, num_challenges_per_cat=10)
    players = PlayerFactory(db_session).n_players(1)
    players[0].player.id = puuids[0]
    with players:
        players[0].add_challenge(name=challenges[0], highscore=1, total=1, avg=10)
    leaderboards_1 = _leaderboards_request(num_challenges=1, num_players=1)
    leaderboards_2 = _leaderboards_request(num_challenges=1, num_players=1)
    assert leaderboards_1.challenges[0].name != leaderboards_2.challenges[0].name


def _leaderboards_request(num_challenges: int, num_players: int):
    response = client.get(
        f"/achievements/leaderboards?challenges={num_challenges}&players={num_players}"
    )
    assert response.status_code == 200
    return Leaderboards(**response.json())
