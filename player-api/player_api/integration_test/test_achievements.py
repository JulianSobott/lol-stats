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


@pytest.fixture
def setup_challenges(db_session: Session):
    challenges = [
        ChallengeClasses(
            name=challenge_1, class_name=category_1, comparison_operator=">", description=challenge_1
        ),
        ChallengeClasses(
            name=challenge_2, class_name=category_2, comparison_operator="<", description=challenge_2
        ),
    ]
    db_session.bulk_save_objects(challenges)
    db_session.commit()


expected_res = Achievements(
        items=[
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
            )
        ]
    )

def test_all_players(db_session: Session, setup_challenges):
    players = PlayerFactory(db_session).n_players(3)
    with players:
        players[0].with_elo(TierEnum.bronze).add_challenge(
            name=challenge_1, highscore=20, total=100, avg=10
        )
        players[1].with_elo(TierEnum.silver).add_challenge(
            name=challenge_1, highscore=30, total=200, avg=5
        )
        players[2].with_elo(TierEnum.grandmaster).add_challenge(
            name=challenge_1, highscore=2, total=2, avg=2
        )
    res = _achievements_reqeust(players[0], query="")
    assert res == expected_res


def test_one_elo(db_session: Session, setup_challenges):
    players = PlayerFactory(db_session).n_players(4)
    with players:
        players[0].with_elo(TierEnum.silver).add_challenge(
            name=challenge_1, highscore=20, total=100, avg=10
        )
        players[1].with_elo(TierEnum.silver).add_challenge(
            name=challenge_1, highscore=30, total=200, avg=5
        )
        players[2].with_elo(TierEnum.silver).add_challenge(
            name=challenge_1, highscore=2, total=2, avg=2
        )
        players[3].with_elo(TierEnum.grandmaster).add_challenge(
            name=challenge_1, highscore=2000, total=40000, avg=100
        )
    res = _achievements_reqeust(players[0], query=f"rank={TierEnum.silver}")
    assert res == expected_res


def test_puuids(db_session: Session, setup_challenges):
    players = PlayerFactory(db_session).n_players(4)
    with players:
        players[0].with_elo(TierEnum.silver).add_challenge(
            name=challenge_1, highscore=20, total=100, avg=10
        )
        players[1].with_elo(TierEnum.silver).add_challenge(
            name=challenge_1, highscore=30, total=200, avg=5
        )
        players[2].with_elo(TierEnum.silver).add_challenge(
            name=challenge_1, highscore=2, total=2, avg=2
        )
        players[3].with_elo(TierEnum.grandmaster).add_challenge(
            name=challenge_1, highscore=2000, total=40000, avg=100
        )
    res = _achievements_reqeust(players[0], query=f"puuids={players[1].player.id}&puuids={players[2].player.id}")
    assert res == expected_res


def _achievements_reqeust(player: Testplayer, query: str) -> Achievements:
    response = client.get(f"/achievements?user={player.player.id}&{query}")
    assert response.status_code == 200
    return Achievements(**response.json())
