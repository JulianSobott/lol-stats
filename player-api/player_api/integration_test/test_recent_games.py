import random
from datetime import datetime, timedelta
import urllib.parse

from fastapi.testclient import TestClient

from player_api.endpoints.recent_games import DEFAULT_GAMES_PER_PAGE
from player_api.integration_test.factories import PlayerFactory, Testplayer
from player_api.main import app
from player_api.models.game import Game, Page, TeamMember

client = TestClient(app)
random.seed(1)


def test_get_most_played_no_games(db_session):
    players = PlayerFactory(db_session).player()
    player = players[0]
    with players:
        pass
    res = _recent_game_request(player)
    assert res.next == ""
    assert len(res.items) == 0


def test_get_most_played_correct_next(db_session):
    players = PlayerFactory(db_session).player()
    player = players[0]
    with players:
        player.play_n_games(DEFAULT_GAMES_PER_PAGE).starting_at(
            datetime(2000, 1, 1)
        ).with_champion("Lux")
    res = _recent_game_request(player)
    start_before = datetime(2000, 1, 1).isoformat()
    assert f"start_before=" + start_before in urllib.parse.unquote(res.next)


def test_get_most_played_correct_games(db_session):
    players = PlayerFactory(db_session).player()
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
    players = PlayerFactory(db_session).player()
    player = players[0]
    with players:
        player.play_n_games(DEFAULT_GAMES_PER_PAGE).starting_at(
            datetime(2000, 1, 1)
        ).with_champion("Lux")
        player.play_n_games(DEFAULT_GAMES_PER_PAGE - 1).starting_at(
            datetime(2000, 1, 2)
        ).with_champion("Azir")
    res = _recent_game_request(player)
    assert len(res.items) == DEFAULT_GAMES_PER_PAGE
    res = _next_game(res)
    assert len(res.items) == DEFAULT_GAMES_PER_PAGE - 1
    res = _next_game(res)
    assert res.next == ""
    assert len(res.items) == 0


def test_contains_team_members(db_session):
    players = PlayerFactory(db_session).player()
    player = players[0]
    with players:
        player.play_n_games(1).with_champion("Lux").starting_at(datetime(2000, 1, 1))
        player.play_n_games(1).with_champion("Aatrox").starting_at(datetime(2000, 1, 2))
    res = _recent_game_request(player)

    assert len(res.items) == 2
    game1 = res.items[0]
    assert len(game1.ally_team) == 5
    assert len(game1.enemy_team) == 5
    assert all(
        map(lambda p: p.champion.name == "Aatrox", game1.ally_team + game1.enemy_team)
    )

    game2 = res.items[1]
    assert len(game2.ally_team) == 5
    assert len(game2.enemy_team) == 5
    assert all(
        map(lambda p: p.champion.name == "Lux", game2.ally_team + game2.enemy_team)
    )


def test_correct_team_colors(db_session):
    players = PlayerFactory(db_session).player()
    player = players[0]
    with players:
        player.play_n_games(1)
    res = _recent_game_request(player)
    ally_color = set(map(lambda m: m.team, res.items[0].ally_team))
    enemy_color = set(map(lambda m: m.team, res.items[0].enemy_team))
    assert len(ally_color) == 1
    assert len(enemy_color) == 1
    assert ally_color.isdisjoint(
        enemy_color
    ), f"should not equal: {ally_color=}, {enemy_color=}"


def _recent_game_request(player: Testplayer) -> Page[Game]:
    response = client.get(f"/players/{player.player.id}/recent-games")
    assert response.status_code == 200
    return Page[Game](**response.json())


def _next_game(res: Page[Game]) -> Page[Game]:
    response = client.get(res.next)
    assert response.status_code == 200
    return Page[Game](**response.json())


def get_own_player(game: Game, player: Testplayer) -> TeamMember | None:
    for member in game.ally_team:
        if member.player.id == player.summoner.puuid:
            return member
    return None
