import os
import psycopg2


class db:
    connection = None
    cursor = None

    def connect(self) -> bool:
        if self.connection is not None:
            return False
        try:
            self.connection = psycopg2.connect(host=os.environ.get('POSTGRES_HOST', 'localhost'),
                                               database='postgres',
                                               user='postgres',
                                               password=os.environ.get('POSTGRES_PASSWORD', 'admin'),
                                               port=5432)
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return True

    def disconnect(self):
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()

    def create_tables(self) -> None:
        self.cursor.execute(open('db_init/schema.sql', 'r').read())
        self.connection.commit()

    def add_summoner(self, puuid: str, level: int, icon_path: str, last_update_time: int):
        sql = """INSERT INTO summoners(puuid, level, icon_path, last_update) VALUES(%s, %s, %s, %s);"""
        self.cursor.execute(sql, (puuid, level, icon_path, last_update_time))
        self.connection.commit()

    def update_summoner_update_time(self, puuid: str, last_update_time: int):
        sql = """UPDATE summoners SET last_update = %s WHERE puuid = %s;"""
        self.cursor.execute(sql, (last_update_time, puuid))
        self.connection.commit()

    def add_summoner_spell(self, id: int, name: str, icon_path:str):
        sql = """INSERT INTO summonerspells(id, name, icon_path) VALUES (%s, %s, %s);"""
        self.cursor.execute(sql, (id, name, icon_path))
        self.connection.commit()

    def clear_summoner_spells(self):
        sql = """DELETE FROM summonerspells;"""
        self.cursor.execute(sql)
        self.connection.commit()

    def add_champion(self, id: int, name: str, icon_path:str):
        sql = """INSERT INTO champions(id, name, icon_path) VALUES (%s, %s, %s);"""
        self.cursor.execute(sql, (id, name, icon_path))
        self.connection.commit()

    def clear_champions(self):
        sql = """DELETE FROM champions;"""
        self.cursor.execute(sql)
        self.connection.commit()

    def add_item(self, id: int, name: str, icon_path:str):
        sql = """INSERT INTO items(id, name, icon_path) VALUES (%s, %s, %s);"""
        self.cursor.execute(sql, (id, name, icon_path))
        self.connection.commit()

    def clear_items(self):
        sql = """DELETE FROM items;"""
        self.cursor.execute(sql)
        self.connection.commit()

    def add_challenge_class(self, name: str, class_name: str, operator: chr):
        sql = """INSERT INTO challengeclasses(name, class, compare_operator) VALUES (%s, %s, %s);"""
        self.cursor.execute(sql, (name, class_name, operator))
        self.connection.commit()

    def add_stat_class(self, name: str, class_name: str, operator: chr):
        sql = """INSERT INTO statclasses(name, class, compare_operator) VALUES (%s, %s, %s);"""
        self.cursor.execute(sql, (name, class_name, operator))
        self.connection.commit()

    def add_challenge(self, name: str, summoner_id: str, total: int, average_per_game: int, highscore: int):
        sql = """INSERT INTO challenges(name, summoner_id, total, average_per_game, highscore) VALUES (%s, %s, %s, %s, %s);"""
        self.cursor.execute(sql, (name, summoner_id, total, average_per_game, highscore))
        self.connection.commit()

    def add_stat(self, name: str, summoner_id: str, total: int, average_per_game: int, highscore: int):
        sql = """INSERT INTO stats(name, summoner_id, total, average_per_game, highscore) VALUES (%s, %s, %s, %s, %s);"""
        self.cursor.execute(sql, (name, summoner_id, total, average_per_game, highscore))
        self.connection.commit()

    def add_game(self, match_id: str, summoner_id: str, start_time: int, duration: int, win: bool, lane: str, stats: str, challenges: str):
        sql = """INSERT INTO challenges(match_id, summoner_id, start_time, duration, win, lane, stats, challenges) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        self.cursor.execute(sql, (match_id, summoner_id, start_time, duration, win, lane, stats, challenges))
        self.connection.commit()