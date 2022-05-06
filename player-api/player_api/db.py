import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
    CheckConstraint,
)
from sqlalchemy.orm import relationship

from player_api.models.player import TierEnum


Base = declarative_base()


class Summoners(Base):
    __tablename__ = "summoners"

    puuid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    win_rate = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    icon_path = Column(String, nullable=False)
    last_update = Column(DateTime, nullable=False)
    tier = Column(Enum(TierEnum))
    rank = Column(Integer, CheckConstraint("rank >= 1 AND rank <= 5"))
    league_points = Column(
        Integer, CheckConstraint("league_points >= 0 AND league_points <= 100")
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
    comparison_operator = Column(String, nullable=False)


class Games(Base):
    __tablename__ = "games"

    match_id = Column(String, primary_key=True)
    summoner_id = Column(
        String, ForeignKey("summoners.puuid"), nullable=False, primary_key=True
    )
    champion_id = Column(Integer, ForeignKey("champions.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    win = Column(Boolean, nullable=False)
    lane = Column(String, nullable=False)
    stats = Column(String, nullable=False)
    challenges = Column(String, nullable=False)

    summoner = relationship("summoners", foreign_keys=[summoner_id])
    champion = relationship("champions", foreign_keys=[champion_id])


def setup_db():
    engine = create_engine(
        f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@"
        f"{os.environ['POSTGRES_HOST']}/postgres"
    )
    engine.connect()
    Base.metadata.create_all(engine)
