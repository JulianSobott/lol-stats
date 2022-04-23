import cassiopeia
from cassiopeia import Patch, Summoner

cassiopeia.set_riot_api_key("")


def add_new_summoner(id: str, region: str):
    summoner: Summoner = cassiopeia.get_summoner(id=id, region=region)
    # check if summoner exists in database
    # if not
    match_history = summoner.match_history(
        begin_time=Patch.from_str("10.12", region=region).start)
    # store match history in db


def update_champions():
    