import os

import cassiopeia
from db_connector import db
from cassiopeia import Patch, Summoner

cassiopeia.set_riot_api_key(os.environ["RIOT_API_KEY"])


class riot_api_connector:
    def __init__(self):
        self.db = db()
        self.db.connect()

    def add_new_summoner(self, id: str, region: str):
        summoner: Summoner = cassiopeia.get_summoner(id=id, region=region)
        # check if summoner exists in database
        # if not
        match_history = summoner.match_history(
            begin_time=Patch.from_str('10.12', region=region).start)
        # store match history in db

    def update_champions(self):
        self.db.clear_champions()
        champions = cassiopeia.get_champions(region='EUW')
        for champ in champions:
            self.db.add_champion(id=champ.id, name=champ.name, icon_path=champ.image.url)

    def update_summoner_spells(self):
        self.db.clear_summoner_spells()
        summoner_spells = cassiopeia.get_summoner_spells(region='EUW')
        for spell in summoner_spells:
            self.db.add_summoner_spell(id=spell.id, name=spell.name, icon_path=spell.image.url)

    def update_items(self):
        self.db.clear_items()
        items = cassiopeia.get_items(region='EUW')
        for item in items:
            self.db.add_item(id=item.id, name=item.name, icon_path=item.image.url)


print("Updating ...")
x = riot_api_connector()
x.update_champions()
x.update_items()
x.update_summoner_spells()
print("Finished updating")
