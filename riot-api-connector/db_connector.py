import os
import psycopg2


class db:
    connection = None
    cursor = None

    def connect(self) -> bool:
        if self.connection is not None:
            return False
        try:
            self.connection = psycopg2.connect(host=os.environ.get('POSTGRES_HOST', 'lol-stats.de'),
                                               database='postgres',
                                               user='postgres',
                                               password='7iF5tCZ84KFW4CxtZAz0K21eLbYjUK8Tdiln4XIUImUszzdLWIj1tuuxcIWamEmD',
                                               #    password=os.environ.get(
                                               #    'POSTGRES_PASSWORD', 'admin'),
                                               port=5432)
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return True

    def disconnect(self) -> None:
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()

    def create_tables(self) -> None:
        self.cursor.execute(open('db_init/schema.sql', 'r').read())
        self.connection.commit()

    def add_summoner(self, puuid: str, name: str, level: int, icon_path: str, last_update_time: int) -> None:
        sql = """INSERT INTO summoners(puuid, name, level, icon_path, last_update) VALUES(%s, %s, %s, %s, %s);"""
        self.cursor.execute(
            sql, (puuid, name, level, icon_path, last_update_time))
        self.connection.commit()

    def update_summoner_update_time(self, puuid: str, last_update_time: int) -> None:
        sql = """UPDATE summoners SET last_update = %s WHERE puuid = %s;"""
        self.cursor.execute(sql, (last_update_time, puuid))
        self.connection.commit()

    def get_summoner(self, puuid: str):
        sql = """SELECT * FROM summoners WHERE puuid = %s;"""
        self.cursor.execute(sql, (puuid,))
        return self.cursor.fetchone()

    def add_summoner_icon(self, id: int, icon_path: str) -> None:
        sql = """INSERT INTO summonericons(id, icon_path) VALUES (%s, %s);"""
        self.cursor.execute(sql, (id, icon_path))
        self.connection.commit()

    def clear_summoner_icons(self) -> None:
        sql = """DELETE FROM summonericons;"""
        self.cursor.execute(sql)
        self.connection.commit()

    def add_summoner_spell(self, id: int, name: str, icon_path: str) -> None:
        sql = """INSERT INTO summonerspells(id, name, icon_path) VALUES (%s, %s, %s);"""
        self.cursor.execute(sql, (id, name, icon_path))
        self.connection.commit()

    def clear_summoner_spells(self) -> None:
        sql = """DELETE FROM summonerspells;"""
        self.cursor.execute(sql)
        self.connection.commit()

    def add_champion(self, id: int, name: str, icon_path: str) -> None:
        sql = """INSERT INTO champions(id, name, icon_path) VALUES (%s, %s, %s);"""
        self.cursor.execute(sql, (id, name, icon_path))
        self.connection.commit()

    def clear_champions(self) -> None:
        sql = """DELETE FROM champions;"""
        self.cursor.execute(sql)
        self.connection.commit()

    def add_item(self, id: int, name: str, icon_path: str) -> None:
        sql = """INSERT INTO items(id, name, icon_path) VALUES (%s, %s, %s);"""
        self.cursor.execute(sql, (id, name, icon_path))
        self.connection.commit()

    def clear_items(self) -> None:
        sql = """DELETE FROM items;"""
        self.cursor.execute(sql)
        self.connection.commit()

    def add_challenge_class(self, name: str, class_name: str, description: str, operator: chr) -> None:
        sql = """INSERT INTO challengeclasses(name, class, description, comparison_operator) VALUES (%s, %s, %s, %s);"""
        self.cursor.execute(sql, (name, class_name, description, operator))
        self.connection.commit()

    def get_challenge_class(self, name: str):
        sql = """SELECT * FROM challengeclasses WHERE name = %s"""
        self.cursor.execute(sql, (name,))
        return self.cursor.fetchone()

    def clear_challenge_classes(self) -> None:
        sql = """DELETE FROM challengeclasses;"""
        self.cursor.execute(sql)
        self.connection.commit()

    def add_challenge(self, name: str, summoner_id: str, total: float, average_per_game: float, highscore: float) -> None:
        try:
            sql = """INSERT INTO challenges(name, summoner_id, total, average_per_game, highscore) VALUES (%s, %s, %s, %s, %s);"""
            self.cursor.execute(sql, (name, summoner_id, float(total),
                                float(average_per_game), float(highscore)))
            self.connection.commit()
        except (TypeError) as error:
            print(f'Error adding challenge {name} to database')

    def update_challenge(self, name: str, puuid: str, total: float, average_per_game: float, highscore: float) -> None:
        try:
            sql = """UPDATE challenges SET total = %s, average_per_game = %s, highscore = %s WHERE name = %s AND summoner_id = %s;"""
            self.cursor.execute(
                sql, (float(total), float(average_per_game), float(highscore), name, puuid))
            self.connection.commit()
        except (TypeError) as error:
            print(f'Error updating challenge {name} in database')

    def get_challenge_entry(self, name: str, puuid: str):
        sql = """SELECT * FROM challenges WHERE name = %s AND summoner_id = %s;"""
        self.cursor.execute(sql, (name, puuid))
        return self.cursor.fetchone()

    def add_game(self, match_id: str, summoner_id: str, champ_id: int, start_time: int, duration: int, win: bool, lane: str, challenges: str) -> None:
        sql = """INSERT INTO games(match_id, summoner_id, champ_id, start_time, duration, win, lane, challenges) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        self.cursor.execute(sql, (match_id, summoner_id, champ_id,
                            start_time, duration, win, lane, challenges))
        self.connection.commit()

    def has_game(self, match_id: str, summoner_id: str) -> bool:
        sql = """SELECT COUNT(1) FROM games WHERE match_id = %s AND summoner_id = %s"""
        self.cursor.execute(sql, (match_id, summoner_id))
        x = self.cursor.fetchone()[0]
        print(x, match_id, summoner_id)
        return x > 0

    def get_games_played_count(self, puuid: str) -> int:
        sql = """SELECT COUNT(summoner_id) FROM games WHERE summoner_id = %s;"""
        self.cursor.execute(sql, (puuid,))
        return self.cursor.fetchone()
