import time
import traceback

import cassiopeia as cass
from cassiopeia import Summoner, Patch, MatchHistory, Match, GameType
from cassiopeia.core.match import Participant

from db_connector import db

import challenges


def get_match_history(summoner: Summoner) -> MatchHistory:
    # TODO currently cass.get_match_history broken, returns only most recent 20 games
    total_matches = 0
    history = cass.get_match_history(
        continent=summoner.region.continent,
        region=summoner.region,
        platform=summoner.region.platform,
        puuid=summoner.puuid,
        begin_time=Patch.from_str('10.12', region=summoner.region).start,
        begin_index=total_matches,
        end_index=total_matches+100)
    return history


def add_missing_games_to_db(db: db, match_history: MatchHistory, puuid: str):
    mh_start_time = time.time()
    c = challenges.Challenges()
    i = 0
    for match in match_history:
        if match.game_type != GameType.matched:
            continue
        if db.has_game(match_id=match.id, summoner_id=puuid):
            continue
        start_time = time.time()
        try:
            add_game_to_db(db=db, match=match, puuid=puuid, c=c)
        except Exception as e:
            print(e, e.args)
            print(traceback.format_exc())
        yield i, len(match_history)
        i += 1
        print(f'[INFO] Imported game in {time.time() - start_time}s')
    print(f'[INFO] Imported match history in {time.time() - mh_start_time}s')


def add_game_to_db(db: db, match: Match, puuid: str, c: challenges.Challenges):
    for participant in match.participants:
        if participant.summoner.puuid == 'BOT':
            continue
        if db.has_game(match_id=match.id, summoner_id=participant.summoner.puuid):
            continue
        if not db.has_summoner(puuid=participant.summoner.puuid):
            summoner: Summoner = participant.summoner
            db.add_summoner(puuid=summoner.puuid, region_id=summoner.id, name=summoner.name, level=None,
                            icon_path=None, tier=None, division=None, last_update_time=None)
        if participant.side == 100:
            win = match.blue_team.win
            side = 'blue'
        else:
            win = match.red_team.win
            side = 'red'
        db.add_game(match_id=match.id, summoner_id=participant.summoner.puuid, champ_id=participant.champion.id, start_time=match.start.int_timestamp,
                    duration=match.duration.seconds, team=side, win=win, lane=participant.individual_position.value, challenges=c.get_json_string(participant.stats))
        c.store_challenges(db=db, stats=participant.stats,
                           puuid=participant.summoner.puuid)
