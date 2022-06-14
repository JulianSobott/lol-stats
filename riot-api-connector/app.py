import logging.config
from pathlib import Path

import yaml

import playerImportRequest
import summoner
from db_connector import db
import time
from threading import Thread
import os
import cassiopeia
import static_data

with open(Path(__file__).parent.joinpath("logging.yml"), 'rt') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

cassiopeia.set_riot_api_key(os.environ["RIOT_API_KEY"])


class riot_api_connector:
    def __init__(self):
        self.db = db()
        self.db.connect()

    def update_loop(self):
        while True:
            try:
                if self.patch_changed():
                    logger.info("msg='new patch available. updating static db data'")
                    self.add_patch()
            except Exception as exception:
                logger.error(f"msg='add_patch failed' {exception=}")
            logger.info("Updating ...")
            try:
                summoner.update_all(db=self.db, region='EUW')
            except Exception as exception:
                logger.error(f"msg='Update all failed' {exception=}")
            logger.info("Finished updating")
            time.sleep(300)

    def patch_changed(self) -> bool:
        last = self.db.get_last_patch()
        if not last:
            return True
        return last[0] == str(cassiopeia.Patch.latest(region='EUW'))

    def add_patch(self):
        self.db.add_patch(patch=str(cassiopeia.Patch.latest(region='EUW')))
        static_data.update_champions(self.db)
        static_data.update_items(self.db)
        static_data.update_summoner_icons(self.db)
        static_data.update_summoner_spells(self.db)


x = riot_api_connector()
grpc_thread = Thread(target=playerImportRequest.serve,
                     args=(x.db, summoner.update_summoner_by_puuid))
grpc_thread.start()
x.update_loop()
