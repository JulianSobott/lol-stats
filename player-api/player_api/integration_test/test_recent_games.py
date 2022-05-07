import random
from datetime import datetime, timedelta
import urllib.parse

from fastapi.testclient import TestClient

from integration_test.factories import PlayerFactory, Testplayer, DEFAULT_GAME_LENGTH
from main import DEFAULT_GAMES_PER_PAGE, app
from models.game import Game, Page, TeamMember

client = TestClient(app)
random.seed(1)


def test_get_most_played_no_games(db_session):
    players = PlayerFactory().player()
    player = players[0]
    with players:
        pass
    res = _recent_game_request(player)
    assert res.next == ""
    assert len(res.items) == 0


def test_get_most_played_correct_next(db_session):
    players = PlayerFactory().player()
    player = players[0]
    with players:
        player.play_n_games(DEFAULT_GAMES_PER_PAGE).starting_at(
            datetime(2000, 1, 1)
        ).with_champion("Lux")
    res = _recent_game_request(player)
    start_after = (
        datetime(2000, 1, 1)
        + timedelta(minutes=(DEFAULT_GAMES_PER_PAGE - 1) * DEFAULT_GAME_LENGTH)
    ).isoformat()
    assert f"start_after=" + start_after in urllib.parse.unquote(res.next)


def test_get_most_played_correct_games(db_session):
    players = PlayerFactory().player()
    player = players[0]
    with players:
        player.play_n_games(DEFAULT_GAMES_PER_PAGE).starting_at(
            datetime(2000, 1, 1)
        ).with_champion("Lux")
        player.play_n_games(DEFAULT_GAMES_PER_PAGE).starting_at(
            datetime(2000, 1, 2)
        ).with_champion("Azir")
    res = _recent_game_request(player)
    assert len(res.items) == DEFAULT_GAMES_PER_PAGE
    for game in res.items:
        own_player = get_own_player(game, player)
        assert own_player is not None
        assert own_player.champion.name == "Azir"


def test_get_most_played_pagination(db_session):
    players = PlayerFactory().player()
    player = players[0]
    with players:
        player.play_n_games(DEFAULT_GAMES_PER_PAGE).starting_at(
            datetime(2000, 1, 1)
        ).with_champion("Lux")
        player.play_n_games(DEFAULT_GAMES_PER_PAGE).starting_at(
            datetime(2000, 1, 2)
        ).with_champion("Azir")
    res = _recent_game_request(player)
    assert len(res.items) == DEFAULT_GAMES_PER_PAGE
    res = _recent_game_request(player)
    assert len(res.items) == DEFAULT_GAMES_PER_PAGE
    res = _recent_game_request(player)


def _recent_game_request(player: Testplayer) -> Page[Game]:
    response = client.get(f"/players/{player.name}/recent-games")
    assert response.status_code == 200
    return Page[Game](**response.json())


def get_own_player(game: Game, player: Testplayer) -> TeamMember | None:
    for member in game.ally_team:
        if member.player.id == player.summoner.puuid:
            return member
    return None
