import os
from enum import Enum

import requests

from player_api.log import get_logger
from player_api.models.player import PlayerId, PlayerName
from player_api.models.player import BasicPlayer

logger = get_logger(__name__)


def find_player_in_riot_api_by(
    player: PlayerId | PlayerName, search: "SearchTerm"
) -> BasicPlayer | None:
    region = "euw1"
    response = requests.get(
        f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-{search.value}/{player}",
        headers={"X-Riot-Token": os.environ.get("RIOT_API_KEY")},
    )
    if not response.ok:
        if response.status_code != 404:
            logger.warning(
                f"Received error status code from riot api. "
                f"{response.request.url=} {response.status_code=} {response.text}"
            )
        return None
    data = response.json()
    return BasicPlayer(
        id=data["puuid"],
        player_icon_path="",
        name=data["name"],
        level=data["summonerLevel"],
        rank=None,
        imported=False,
    )


class SearchTerm(str, Enum):
    name = "name"
    id = "puuid"
