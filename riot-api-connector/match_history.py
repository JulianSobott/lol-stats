import logging
import os

import time
import traceback

import cassiopeia as cass
from cassiopeia import Summoner, Patch, MatchHistory, Match, GameType, Map
from cassiopeia.core.match import Participant, Side
import riotwatcher
from riotwatcher import LolWatcher, ApiError
from riotwatcher._apis.league_of_legends import MatchApiV5
from sentry_sdk import capture_exception

from db_connector import db

import challenges
from riotwatcherWrapper import call_with_retry

logger = logging.getLogger(__name__)

lol_watcher = LolWatcher('RGAPI-ba00cb63-7be0-4e50-8610-eb749b1ea70d')

IMPORT_LIMIT_MATCHES = int(os.environ.get("IMPORT_LIMIT_MATCHES", 20))


def get_match_ids(puuid: str, start_time: int | None = None):
    end_time = 9900000000 if start_time is None else None   # Start from end and pick value in the far future
    return _get_mh(region='euw1', puuid=puuid, start_time=start_time, count=IMPORT_LIMIT_MATCHES, end_time=end_time)


@call_with_retry(max_retries=5)
def _get_mh(region: str, puuid: str, start_time: int | None, count: int, end_time: int | None):
    return lol_watcher.match.matchlist_by_puuid(region=region, puuid=puuid, start_time=start_time, count=count, end_time=end_time)


def add_missing_games_to_db(db: db, match_ids, puuid: str):
    mh_start_time = time.time()
    c = challenges.Challenges()
    i = 0
    for match_id in match_ids:
        match: Match = cass.get_match(id=match_id, region='EUW')
        if match.game_type != GameType.matched or match.map.id not in [1, 2, 11]:    # Summoners Rift
            continue
        if db.has_game(match_id=match.id, summoner_id=puuid):
            continue
        start_time = time.time()
        try:
            add_game_to_db(db=db, match=match, puuid=puuid, c=c)
        except Exception as e:
            capture_exception(e)
            print(e, e.args)
            print(traceback.format_exc())
        yield i, len(match_ids)
        i += 1
        logger.info(f'method=add_missing_games_to_db msg="imported game in {time.time() - start_time}s"')
    logger.info(f'method=add_missing_games_to_db msg="Imported match history in {time.time() - mh_start_time}s"')


def add_game_to_db(db: db, match: Match, puuid: str, c: challenges.Challenges):
    for participant in match.participants:
        if participant.summoner.puuid == 'BOT':
            continue
        if db.has_game(match_id=match.id, summoner_id=participant.summoner.puuid):
            continue
        if not db.has_summoner(puuid=participant.summoner.puuid):
            summoner: Summoner = participant.summoner
            db.add_summoner(puuid=summoner.puuid, region_id=summoner.id, name=summoner.name, level=None,
                            icon_path=None, tier=None, division=None, lp=None, last_update_time=None)
        if participant.side == Side.blue:
            win = match.blue_team.win
            side = 'blue'
        else:
            win = match.red_team.win
            side = 'red'
        try:
            lane = participant.individual_position.value
        except KeyError:
            logger.warning(f"msg='participant with invalid position' {participant.summoner.puuid=} {match.id=}")
            lane = "UNKNOWN"
        db.add_game(match_id=match.id, summoner_id=participant.summoner.puuid, champ_id=participant.champion.id, start_time=match.start.int_timestamp,
                    duration=match.duration.seconds, team=side, win=win, lane=lane, challenges=c.get_json_string(participant.stats))
        if participant.stats:
            if participant.stats.challenges is None:
                logger.warning(f"msg='no challenges for participant. Importing only stats' {participant.summoner.puuid=} {match.id=}")
            c.store_challenges(db=db, stats=participant.stats,
                               puuid=participant.summoner.puuid)
        else:
            logger.warning(f"msg='no stats for participant' {participant.summoner.puuid=} {match.id=}")
