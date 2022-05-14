import json
import cassiopeia
import re

from db_connector import db
from cassiopeia.core.match import ParticipantStats


class Challenges:
    operator_cache = None

    wrong_fields = {
        'summoner_1_casts': 'summoner_spell_1_casts',
        'summoner_2_casts': 'summoner_spell_2_casts',
        'time_c_cing_others': 'time_CCing_others',
        'total_time_c_c_dealt': 'total_time_cc_dealt',
        'champ_level': 'level',
        'game_ended_in_early_surrender': 'ended_in_early_surrender'
    }

    def __init__(self) -> None:
        with open('db_init/challengeClasses.json') as file:
            self.classes = json.load(file)

    def store_classes_in_db(self, db: db) -> None:
        db.clear_challenge_classes()
        for class_ in self.classes:
            for challenge in self.classes[class_]:
                db.add_challenge_class(name=challenge['name'], class_name=class_,
                                       description=challenge['description'], operator=challenge['operator'])

    def store_challenges(self, db: db, stats: ParticipantStats, puuid: str):
        total_games = db.get_games_played_count(puuid=puuid)
        total_games = total_games[0]
        rows = db.get_challenge_entries(puuid=puuid)
        old_values = {}
        for row in rows:
            old_values[row[0]] = (row[2], row[3], row[4])
        for class_ in self.classes:
            for challenge in self.classes[class_]:
                new_stat = self.get_stat(
                    challenge_name=challenge['name'], stats=stats)
                if challenge['name'] in old_values:
                    old_value = old_values[challenge['name']]
                    if self.operator_cache is None:
                        rows = db.get_challenge_classes()
                        self.operator_cache = {}
                        for row in rows:
                            self.operator_cache[row[0]] = row[3]
                    # operator = db.get_challenge_class(
                    #     name=challenge['name'])[3]
                    operator = self.operator_cache[challenge['name']]
                    db.update_challenge(name=challenge['name'], puuid=puuid,
                                        total=new_stat + old_value[0], average_per_game=(new_stat + (total_games - 1) * old_value[1]) / total_games,
                                        highscore=max(new_stat, old_value[2]) if operator == '>' else min(new_stat, old_value[2]), no_commit=True)
                else:
                    db.add_challenge(
                        name=challenge['name'], summoner_id=puuid, total=new_stat, average_per_game=new_stat, highscore=new_stat, no_commit=True)
        db.commit()

    def get_json_string(self, stats: ParticipantStats) -> str:
        dict = {}
        for class_ in self.classes:
            for challenge in self.classes[class_]:
                result = self.get_stat(
                    challenge_name=challenge['name'], stats=stats)
                # some stats that are not present in the current game are stuck on lazy loading
                if callable(result):
                    result = 0
                dict[challenge['name']] = result
        return json.dumps(dict)

    def get_stat(self, challenge_name: str, stats: ParticipantStats):
        if challenge_name[0] == '-':
            name = self.camel_to_snake(challenge_name[1:])
            if name in self.wrong_fields:
                name = self.wrong_fields[name]
            try:
                new_stat = getattr(stats, name)
            except (AttributeError) as error:
                return 0
        else:
            try:
                new_stat = getattr(stats, 'challenges')[challenge_name]
            except (KeyError) as error:
                return 0
        return new_stat

    def camel_to_snake(self, snake: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z0-9])', '_', snake).lower()
