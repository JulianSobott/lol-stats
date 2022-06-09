import playerImportRequest
import summoner
from db_connector import db
import time
from threading import Thread
import os
import cassiopeia


cassiopeia.set_riot_api_key(os.environ["RIOT_API_KEY"])


class riot_api_connector:
    def __init__(self):
        self.db = db()
        self.db.connect()

    def update_loop(self):
        while True:
            print("Updating ...")
            summoner.update_all(db=self.db, region='EUW')
            print("Finished updating")
            time.sleep(300)


x = riot_api_connector()
grpc_thread = Thread(target=playerImportRequest.serve,
                     args=(x.db, summoner.update_summoner_by_puuid))
grpc_thread.start()
x.update_loop()
# x.update_summoner_by_name(name='LinkX20', region='EUW')
# match_history.riot_watcher_mh(
#    puuid='i6rhuj9rVlNXt0WRoGzMelbaGItog4yYs6mC8yZXQOY2rpuY68virbdeyvnoptwJ07u1cgZKW1tBPA', start_time=1627776000)
# x.update_summoner_by_puuid(
#     'i6rhuj9rVlNXt0WRoGzMelbaGItog4yYs6mC8yZXQOY2rpuY68virbdeyvnoptwJ07u1cgZKW1tBPA')
# x.update_all(region='EUW')
# playerImportRequest.serve(lambda y: x.update_summoner_by_region_id(id=y, region='EUW'))
# x.update_all(region='EUW')
# x.db.create_tables()
#x.update_summoner_by_name('LinkX20', region='EUW')
# x.get_summoner('gravitysuit', region='EUW')
# x.get_summoner('LinkX20', 'EUW')
# static_data.update_summoner_icons(x.db)
