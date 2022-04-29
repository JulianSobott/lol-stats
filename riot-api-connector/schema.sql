CREATE TABLE IF NOT EXISTS Summoners (
   puuid        TEXT    PRIMARY KEY     NOT NULL,
   level        INT                     NOT NULL,
   icon_path    TEXT                    NOT NULL,
   last_update  INT                     NOT NULL
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


CREATE TABLE IF NOT EXISTS ChallengeClasses (
   name		TEXT	PRIMARY KEY	NOT NULL,
   class	TEXT			NOT NULL,
   comparison_operator TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS StatClasses (
   name		TEXT	PRIMARY KEY	NOT NULL,
   class	TEXT			NOT NULL,
   comparison_operator TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Challenges (
   name         TEXT                    NOT NULL,
   summoner_id  TEXT                    NOT NULL,
   total        INT                     NOT NULL,
   average_per_game INT                 NOT NULL,
   highscore    INT                     NOT NULL,
   PRIMARY KEY (name, summoner_id),
   FOREIGN KEY (name)
        REFERENCES ChallengeClasses(name),
   FOREIGN KEY (summoner_id)
        REFERENCES Summoners (puuid)
);

CREATE TABLE IF NOT EXISTS Stats (
   name         TEXT                    NOT NULL,
   summoner_id  TEXT                    NOT NULL,
   total        INT                     NOT NULL,
   average_per_game INT                 NOT NULL,
   highscore    INT                     NOT NULL,
   PRIMARY KEY (name, summoner_id),
   FOREIGN KEY (name)
        REFERENCES StatClasses(name),
   FOREIGN KEY (summoner_id)
        REFERENCES Summoners (puuid)
);

CREATE TABLE IF NOT EXISTS Games (
   match_id     TEXT                    NOT NULL,
   summoner_id  TEXT                    NOT NULL,
   start_time   INT                     NOT NULL,
   duration     INT                     NOT NULL,
   win          BOOLEAN                 NOT NULL,
   lane         TEXT                    NOT NULL,
   stats        TEXT                    NOT NULL,
   challenges   TEXT                    NOT NULL,
   PRIMARY KEY (match_id, summoner_id),
   FOREIGN KEY (summoner_id)
        REFERENCES Summoners (puuid)
);