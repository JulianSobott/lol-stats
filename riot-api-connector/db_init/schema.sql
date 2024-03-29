CREATE TABLE IF NOT EXISTS Summoners (
   puuid        TEXT    PRIMARY KEY     NOT NULL,
   region_id    TEXT                            ,
   name         TEXT                    NOT NULL,
   level        INT                             ,
   icon_path    TEXT                            ,
   tier         TEXT                            ,
   division     TEXT                            ,
   last_update  INT                             ,
   league_points INT
);

CREATE TABLE IF NOT EXISTS SummonerSpells (
   id           INT     PRIMARY KEY     NOT NULL,
   name         TEXT                    NOT NULL,
   icon_path    TEXT                    NOT NULL
);

CREATE TABLE IF NOT EXISTS Champions (
   id           INT     PRIMARY KEY     NOT NULL,
   name         TEXT                    NOT NULL,
   icon_path    TEXT                    NOT NULL
);

CREATE TABLE IF NOT EXISTS Items (
   id           INT     PRIMARY KEY     NOT NULL,
   name         TEXT                    NOT NULL,
   icon_path    TEXT                    NOT NULL
);

CREATE TABLE IF NOT EXISTS SummonerIcons (
   id           INT     PRIMARY KEY     NOT NULL,
   icon_path    TEXT                    NOT NULL
);

CREATE TABLE IF NOT EXISTS ChallengeClasses (
   name		TEXT	PRIMARY KEY	NOT NULL,
   class	TEXT			NOT NULL,
   description TEXT NOT NULL,
   comparison_operator TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Challenges (
   name         TEXT                    NOT NULL,
   summoner_id  TEXT                    NOT NULL,
   total        FLOAT                     NOT NULL,
   average_per_game FLOAT                 NOT NULL,
   highscore    FLOAT                     NOT NULL,
   PRIMARY KEY (name, summoner_id),
   FOREIGN KEY (name)
        REFERENCES ChallengeClasses(name),
   FOREIGN KEY (summoner_id)
        REFERENCES Summoners (puuid)
);

CREATE TABLE IF NOT EXISTS Games (
   match_id     TEXT                    NOT NULL,
   summoner_id  TEXT                    NOT NULL,
   champ_id     INT                     NOT NULL,
   start_time   INT                     NOT NULL,
   duration     INT                     NOT NULL,
   team         TEXT                    NOT NULL,
   win          BOOLEAN                 NOT NULL,
   lane         TEXT                    NOT NULL,
   challenges   TEXT                    NOT NULL,
   PRIMARY KEY (match_id, summoner_id),
   FOREIGN KEY (summoner_id)
        REFERENCES Summoners (puuid),
   FOREIGN KEY (champ_id)
        REFERENCES Champions (id)
);

CREATE TABLE IF NOT EXISTS Patches (
   patch        TEXT                    NOT NULL,
   added        FLOAT                   NOT NULL
);
