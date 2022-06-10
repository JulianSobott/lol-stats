import os
import time
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Enum,
    CheckConstraint,
    Float,
)
from sqlalchemy.orm import relationship, sessionmaker

from player_api.models.game import TeamSide
from player_api.models.player import TierEnum

db_user = os.environ.get("POSTGRES_USER", "postgres")
db_pw = os.environ.get("POSTGRES_PASSWORD", "postgres")
db_host = os.environ.get("POSTGRES_HOST", "localhost")
db_type = os.environ.get("DB_TYPE", "postgresql")
db_database = os.environ.get("DB_DATABASE", "postgres")

engine = create_engine(
    f"{db_type}://{db_user}:{db_pw}@{db_host}/{db_database}",
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


class DivisionEnum(str, enum.Enum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"


class Summoners(Base):
    __tablename__ = "summoners"

    puuid = Column(String, primary_key=True)
    region_id = Column(String)
    name = Column(String, nullable=False)
    level = Column(Integer, nullable=True)
    icon_path = Column(String, nullable=True)
    last_update = Column(Integer, nullable=True)
    tier = Column(Enum(TierEnum))
    division = Column(Enum(DivisionEnum))
    league_points = Column(
        Integer, CheckConstraint("league_points >= 0")
    )


class SummonerSpells(Base):
    __tablename__ = "summonerspells"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    icon_path = Column(String, nullable=False)


class Champions(Base):
    __tablename__ = "champions"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    icon_path = Column(String, nullable=False)


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    icon_path = Column(String, nullable=False)


class ChallengeClasses(Base):
    __tablename__ = "challengeclasses"

    name = Column(String, primary_key=True)
    class_name = Column(String, nullable=False, name="class")
    description = Column(String, nullable=False)
    comparison_operator = Column(String, nullable=False)


class Challenges(Base):
    __tablename__ = "challenges"

    name = Column(
        String, ForeignKey("challengeclasses.name"), nullable=False, primary_key=True
    )
    summoner_id = Column(
        String, ForeignKey("summoners.puuid"), nullable=False, primary_key=True
    )
    total = Column(Float)
    average_per_game = Column(Float)
    highscore = Column(Float)

    summoner = relationship("Summoners", foreign_keys=[summoner_id])
    challenge_class = relationship("ChallengeClasses", foreign_keys=[name])


class Games(Base):
    __tablename__ = "games"

    match_id = Column(String, primary_key=True)
    summoner_id = Column(
        String, ForeignKey("summoners.puuid"), nullable=False, primary_key=True
    )
    champ_id = Column(Integer, ForeignKey("champions.id"), nullable=False)
    start_time = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    team = Column(Enum(TeamSide), nullable=False)
    win = Column(Boolean, nullable=False)
    lane = Column(String, nullable=False)
    challenges = Column(String, nullable=False)

    summoner = relationship("Summoners", foreign_keys=[summoner_id])
    champion = relationship("Champions", foreign_keys=[champ_id])


def datetime_to_db(ts: datetime) -> int:
    return int(time.mktime(ts.timetuple()))


def db_to_datetime(ts: int) -> datetime:
    return datetime.fromtimestamp(ts)


def setup_db():
    engine = create_engine(
        f"postgresql://postgres:{os.environ.get('POSTGRES_PASSWORD', 'postgres')}@"
        f"{os.environ.get('POSTGRES_HOST', 'localhost')}/postgres",
    )
    engine.connect()
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    setup_db()
