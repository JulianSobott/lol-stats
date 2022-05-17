import os
import time
import sys

import cassiopeia as cass
from cassiopeia import Patch, Summoner, Match, Rank, Queue, Tier, Division
from cassiopeia.core.match import Participant
from riotwatcher import LolWatcher, ApiError
lol_watcher = LolWatcher('RGAPI-ba00cb63-7be0-4e50-8610-eb749b1ea70d')

from db_connector import db
import static_data
import challenges
import match_history
import playerImportRequest

# cassiopeia.set_riot_api_key(os.environ["RIOT_API_KEY"])
cass.set_riot_api_key('RGAPI-ba00cb63-7be0-4e50-8610-eb749b1ea70d')


class riot_api_connector:
    def __init__(self):
        self.db = db()
        self.db.connect()

    def add_summoner(self, summoner: Summoner):
        self.db.add_summoner(puuid=summoner.puuid, region_id=summoner.id, name=summoner.name, level=summoner.level, tier=summoner.ranks[Queue.ranked_solo_fives].tier.name,
                             division=summoner.ranks[Queue.ranked_solo_fives].division.name, icon_path=summoner.profile_icon().url, last_update_time=time.time())

    def update_summoner(self, summoner: Summoner):
        db_summoner = self.db.get_summoner(puuid=summoner.puuid)
        if db_summoner is None:
            self.add_summoner(summoner=summoner)
            mh = match_history.get_match_history(summoner=summoner)
            match_history.add_missing_games_to_db(
                db=self.db, match_history=mh, puuid=summoner.puuid)
        else:
            last_update = db_summoner[3]
            self.db.update_summoner(puuid=summoner.puuid, name=summoner.name, level=summoner.level, tier=summoner.ranks[Queue.ranked_solo_fives].tier.name,
                                    division=summoner.ranks[Queue.ranked_solo_fives].division.name, icon_path=summoner.profile_icon().url, last_update_time=time.time())
            mh = match_history.get_match_history(summoner=summoner)
            yield from match_history.add_missing_games_to_db(
                db=self.db, match_history=mh, puuid=summoner.puuid)
            # only update games since last update timestamp, currently not possible

    def update_summoner_by_name(self, name: str, region: str):
        self.update_summoner(summoner=cass.get_summoner(
            name=name, region=region))

    def update_summoner_by_region_id(self, id: int, region: str):
        yield from self.update_summoner(summoner=cass.get_summoner(id=id, region=region))

    def update_all(self, region: str) -> None:
        rows = self.db.get_all_full_summoners()
        i = 0
        n = len(rows)
        for row in rows:
            j = (i + 1) / n
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
            sys.stdout.flush()
            self.update_summoner(puuid=row[0], region=region)
            i += 1

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
x.update_summoner_by_name(name='Gemmling', region='EUW')
playerImportRequest.serve(lambda y: x.update_summoner_by_region_id(id=y, region='EUW'))
# x.update_all(region='EUW')
# x.db.create_tables()
#x.update_summoner_by_name('LinkX20', region='EUW')
# x.get_summoner('gravitysuit', region='EUW')
# x.get_summoner('LinkX20', 'EUW')
# static_data.update_summoner_icons(x.db)
print("Finished updating")
