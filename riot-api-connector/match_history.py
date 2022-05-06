from tracemalloc import start
import cassiopeia as cass
from cassiopeia import Summoner, Patch, MatchHistory
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
    c = challenges.Challenges()
    for match in match_history:
        if db.has_game(match_id=match.id, summoner_id=puuid):
            continue
        participant: Participant = match.participants[puuid]
        if participant.side == 100:
            win = match.blue_team.win
        else:
            win = match.red_team.win
        db.add_game(match_id=match.id, summoner_id=puuid, start_time=match.start.int_timestamp, duration=match.duration.seconds,
                    win=win, lane=participant.individual_position.value, challenges=c.get_json_string(participant.stats))
        c.store_challenges(db=db, stats=participant.stats, puuid=puuid)
