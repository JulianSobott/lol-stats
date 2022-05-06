import os
import time

import cassiopeia as cass
from cassiopeia import Patch, Summoner, Match
from cassiopeia.core.match import Participant

from db_connector import db
import static_data
import challenges
import match_history

# cassiopeia.set_riot_api_key(os.environ["RIOT_API_KEY"])
cass.set_riot_api_key('RGAPI-ba00cb63-7be0-4e50-8610-eb749b1ea70d')


class riot_api_connector:
    def __init__(self):
        self.db = db()
        self.db.connect()

    def add_summoner(self, summoner: Summoner):
        self.db.add_summoner(puuid=summoner.puuid, name=summoner.name, level=summoner.level,
                             icon_path=summoner.profile_icon().url, last_update_time=time.time())

    def get_summoner(self, name: str, region: str) -> Summoner:
        summoner: Summoner = cass.get_summoner(name=name, region=region)
        db_summoner = self.db.get_summoner(puuid=summoner.puuid)
        if db_summoner is None:
            self.add_summoner(summoner=summoner)
            mh = match_history.get_match_history(summoner=summoner)
            match_history.add_missing_games_to_db(
                db=self.db, match_history=mh, puuid=summoner.puuid)
        else:
            last_update = db_summoner[3]
            mh = match_history.get_match_history(summoner=summoner)
            match_history.add_missing_games_to_db(
                db=self.db, match_history=mh, puuid=summoner.puuid)
            # only update games since last update timestamp, currently not possible

        return summoner

    # def test(self):
    #     summoner = self.get_summoner('LinkX20', 'EUW')
    #     # self.add_summoner(summoner=summoner)
    #     test: Match = Match(
    #         id='EUW1_5858029465', region='EUW')
    #     c = challenges.Challenges()
    #     self.store_game(test, summoner.puuid)
    #     #c.store_challenges(self.db, test.participants[0].stats, summoner.puuid)

    # def test_match_history(self):
    #     summoner = self.get_summoner('LinkX20', 'EUW')
    #     total_matches = 20
    #     history = cass.get_match_history(
    #         continent=summoner.region.continent,
    #         region=summoner.region,
    #         platform=summoner.region.platform,
    #         puuid=summoner.puuid,
    #         begin_time=Patch.from_str('10.12', region=summoner.region).start,
    #         begin_index=total_matches,
    #         end_index=total_matches+100)
    #     print(history[0].id)
    #     print(len(history))


print("Updating ...")
x = riot_api_connector()
# x.test_match_history()
x.get_summoner('LinkX20', region='EUW')
#x.get_summoner('LinkX20', 'EUW')
# x.db.create_tables()
# static_data.update_summoner_icons(x.db)
# c = challenges.Challenges()
# c.store_classes_in_db(x.db)
print("Finished updating")
