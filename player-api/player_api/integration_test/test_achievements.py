"""
test coverage

- players
    - all players
    - one player
    - two players
- elo
    - all elos
    - one elo
- champions
    - all champions
    - one champion

test strategy:
- for each filter one test -> assert exact
- one test with all permutations -> assert no failure
"""
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from player_api.db import ChallengeClasses
from player_api.integration_test.factories import PlayerFactory, Testplayer
from player_api.models.achievements import (
    Achievements,
    AchievementCategory,
    Achievement,
    AchievementStats,
    AchievementStat,
    Comparison,
)
from player_api.models.player import TierEnum
from player_api.main import app

client = TestClient(app)

challenge_1 = "challenge_1"
challenge_2 = "challenge_2"
category_1 = "category_1"
category_2 = "category_2"

PLAYER_UUID = "ABCDEFG"
PLAYER_ID = "1"

PLAYER_2_UUID = "PLAYER2"
PLAYER_3_UUID = "PLAYER3"


@pytest.fixture
def setup_challenges(db_session: Session):
    challenges = [
        ChallengeClasses(
            name=challenge_1,
            class_name=category_1,
            comparison_operator=">",
            description=challenge_1,
        ),
        ChallengeClasses(
            name=challenge_2,
            class_name=category_2,
            comparison_operator="<",
            description=challenge_2,
        ),
    ]
    db_session.bulk_save_objects(challenges)
    db_session.commit()


@pytest.fixture
def mock_user_api(requests_mock):
    requests_mock.real_http = True
    requests_mock.get(
        f"https://lol-stats.de/api/users/{PLAYER_ID}/achievements",
        json={"status": "success", "achievements": []},
    )
    requests_mock.get(
        f"https://lol-stats.de/api/users/1",
        json={"id": 1, "player_uuid": PLAYER_UUID, "region": "euw"},
    )
    requests_mock.get(
        f"https://lol-stats.de/api/users/{PLAYER_ID}/competitors",
        json=[
            {
                "id": 1,
                "player_uuid": PLAYER_2_UUID,
                "player_name": "",
                "player_stats": None,
            },
            {
                "id": 2,
                "player_uuid": PLAYER_3_UUID,
                "player_name": "",
                "player_stats": None,
            },
        ],
    )


expected_res = Achievements(
    items=[
        AchievementCategory(category="Favourites", achievements=[]),
        AchievementCategory(
            category=category_1,
            achievements=[
                Achievement(
                    fav=False,
                    name=challenge_1,
                    description=challenge_1,
                    you=AchievementStats(
                        max=AchievementStat(value=20, compare=Comparison.BETTER),
                        total=AchievementStat(value=100, compare=Comparison.WORSE),
                        avg=AchievementStat(value=10, compare=Comparison.BETTER),
                    ),
                    other=AchievementStats(
                        max=AchievementStat(
                            value=(30 + 2) / 2, compare=Comparison.WORSE
                        ),
                        total=AchievementStat(
                            value=(200 + 2) / 2, compare=Comparison.BETTER
                        ),
                        avg=AchievementStat(
                            value=(5 + 2) / 2, compare=Comparison.WORSE
                        ),
                    ),
                )
            ],
        ),
    ]
)


def test_all_players(db_session: Session, setup_challenges, mock_user_api):
    players = _prepare_players(db_session, extra_challenger=False)
    res = _achievements_reqeust(players[0], query="")
    assert res == expected_res


def test_one_elo(db_session: Session, setup_challenges, mock_user_api):
    players = _prepare_players(db_session)
    res = _achievements_reqeust(players[0], query=f"rank={TierEnum.SILVER}")
    assert res == expected_res


def test_competitors(db_session: Session, setup_challenges, mock_user_api):
    players = _prepare_players(db_session)
    res = _achievements_reqeust(players[0], query=f"competitors=true")
    assert res == expected_res


def test_favourites(
    db_session: Session, setup_challenges, mock_user_api, requests_mock
):
    requests_mock.get(
        f"https://lol-stats.de/api/users/{PLAYER_ID}/achievements",
        json={"status": "success", "achievements": [challenge_1]},
    )
    players = _prepare_players(db_session)
    res = _achievements_reqeust(players[0], query="")
    assert res.items[0].category == "Favourites"
    assert res.items[0].achievements[0].name == challenge_1
    assert res.items[1].achievements[0].name == challenge_1


def test_invalid_compare(
    db_session: Session, setup_challenges, mock_user_api, requests_mock
):
    players = _prepare_players(db_session)
    res = _achievements_reqeust(players[0], query=f"competitor={PLAYER_UUID}")
    assert len(res.items) == 0


def _prepare_players(db_session: Session, extra_challenger: bool = True):
    players = PlayerFactory(db_session).n_players(4 if extra_challenger else 3)
    players[0].player.id = PLAYER_UUID
    players[1].player.id = PLAYER_2_UUID
    players[2].player.id = PLAYER_3_UUID
    with players:
        players[0].with_elo(TierEnum.SILVER).add_challenge(
            name=challenge_1, highscore=20, total=100, avg=10
        )
        players[1].with_elo(TierEnum.SILVER).add_challenge(
            name=challenge_1, highscore=30, total=200, avg=5
        )
        players[2].with_elo(TierEnum.SILVER).add_challenge(
            name=challenge_1, highscore=2, total=2, avg=2
        )
        if extra_challenger:
            players[3].with_elo(TierEnum.GRANDMASTER).add_challenge(
                name=challenge_1, highscore=2000, total=40000, avg=100
            )
    return players


def _achievements_reqeust(player: Testplayer, query: str) -> Achievements:
    response = client.get(f"/achievements?me={PLAYER_ID}&{query}")
    assert response.status_code == 200
    return Achievements(**response.json())
