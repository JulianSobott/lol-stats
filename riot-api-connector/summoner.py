import logging
import os

from riotwatcher import LolWatcher, ApiError
from sentry_sdk import capture_exception

from db_connector import db
import time
import cassiopeia as cass
import sys
import match_history
from riotwatcherWrapper import call_with_retry

logger = logging.getLogger(__name__)

lol_watcher = LolWatcher(os.environ["RIOT_API_KEY"])


def add_summoner(db: db, summoner, rank, icon_url):
    db.add_summoner(puuid=summoner['puuid'], region_id=summoner['id'], name=summoner['name'], level=summoner['summonerLevel'], tier=rank['tier'],
                    division=rank['rank'], icon_path=icon_url, lp=rank['leaguePoints'], last_update_time=time.time())


def update_summoner(db: db, summoner):
    logger.debug(f"method=update_summoner {summoner=}")
    icon_url = db.get_summoner_icon_url(summoner['profileIconId'])
    rank = _get_rank(summoner['id'])
    if db_summoner := db.get_summoner(puuid=summoner['puuid']):
        last_update = db_summoner[3]
        db.update_summoner(puuid=summoner['puuid'], name=summoner['name'], level=summoner['summonerLevel'], tier=rank['tier'],
                           division=rank['rank'], icon_path=icon_url, lp=rank['leaguePoints'], last_update_time=time.time())
        mh = match_history.get_match_ids(
            puuid=summoner['puuid'], start_time=last_update)
        yield from match_history.add_missing_games_to_db(
            db=db, match_ids=mh, puuid=summoner['puuid'])
    else:
        add_summoner(db=db, summoner=summoner, rank=rank, icon_url=icon_url)
        mh = match_history.get_match_ids(
            puuid=summoner['puuid'])
        yield from match_history.add_missing_games_to_db(
            db=db, match_ids=mh, puuid=summoner['puuid'])


def update_summoner_by_name(db: db, name: str, region: str):
    yield from update_summoner(db=db, summoner=_get_summoner_by_name(name=name))


def update_summoner_by_region_id(db: db, id: int, region: str):
    yield from update_summoner(db=db, summoner=_get_summoner_by_region_id(id=id))


def update_summoner_by_puuid(db: db, puuid: str):
    yield from update_summoner(db=db, summoner=_get_summoner_by_puuid(puuid=puuid))


def update_all(db: db, region: str) -> None:
    rows = db.get_all_full_summoners()
    i = 0
    n = len(rows)
    for row in rows:
        j = (i + 1) / n
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%%\n" % ('='*int(20*j), 100*j))
        sys.stdout.flush()
        try:
            for _ in update_summoner_by_region_id(db=db, id=row[1], region=region):
                pass
        except Exception as exception:
            capture_exception(exception)
            logging.error(f"msg='Update summoner failed' {exception=} id={row[1]}")
        i += 1


@call_with_retry(max_retries=5)
def _get_summoner_by_puuid(puuid: str):
    return lol_watcher.summoner.by_puuid(region='euw1', encrypted_puuid=puuid)


@call_with_retry(max_retries=5)
def _get_summoner_by_region_id(id: str):
    return lol_watcher.summoner.by_id(region='euw1', encrypted_summoner_id=id)


@call_with_retry(max_retries=5)
def _get_summoner_by_name(name: str):
    return lol_watcher.summoner.by_name(region='euw1', summoner_name=name)


@call_with_retry(max_retries=5)
def _get_rank(id: str):
    rank = lol_watcher.league.by_summoner(
        region='euw1', encrypted_summoner_id=id)
    if len(rank) == 0:
        return {'tier': 'UNRANKED', 'rank': None, 'leaguePoints': None}
    for s in rank:
        if s['queueType'] == 'RANKED_SOLO_5x5':
            rank = s
            break
    else:
        rank = rank[0]
    return rank
