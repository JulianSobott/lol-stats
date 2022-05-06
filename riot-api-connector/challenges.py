import json
import cassiopeia
import re

from db_connector import db
from cassiopeia.core.match import ParticipantStats


class Challenges:
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
        print(total_games)
        total_games = total_games[0]
        for class_ in self.classes:
            for challenge in self.classes[class_]:
                row = db.get_challenge_entry(
                    name=challenge['name'], puuid=puuid)
                new_stat = self.get_stat(
                    challenge_name=challenge['name'], stats=stats)
                if row is None:
                    db.add_challenge(
                        name=challenge['name'], summoner_id=puuid, total=new_stat, average_per_game=new_stat, highscore=new_stat)
                else:
                    old_values = db.get_challenge_entry(
                        name=challenge['name'], puuid=puuid)
                    operator = db.get_challenge_class(
                        name=challenge['name'])[3]
                    db.update_challenge(name=challenge['name'], puuid=puuid,
                                        total=new_stat + old_values[2], average_per_game=(new_stat + (total_games - 1) * old_values[3]) / total_games,
                                        highscore=max(new_stat, old_values[4]) if operator == '>' else min(new_stat, old_values[4]))

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
                print(name)
                return 0
        else:
            try:
                new_stat = getattr(stats, 'challenges')[challenge_name]
            except (KeyError) as error:
                return 0
        return new_stat

    def camel_to_snake(self, snake: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z0-9])', '_', snake).lower()
