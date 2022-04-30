import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine(f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@"
                       f"{os.environ['POSTGRES_HOST']}/postgres")
connection = engine.connect()

Base = declarative_base()


class Summoners(Base):
    __tablename__ = "summoners"

    puuid = Column(String, primary_key=True)
    level = Column(Integer, nullable=False)
    icon_path = Column(String, nullable=False)
    last_update = Column(String, nullable=False)


class SummonerSpells(Base):
    __tablename__ = "SummonerSpells"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    icon_path = Column(String, nullable=False)


class Champions(Base):
    __tablename__ = "Champions"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    icon_path = Column(String, nullable=False)


class Items(Base):
    __tablename__ = "Items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    icon_path = Column(String, nullable=False)


class ChallengeClasses(Base):
    __tablename__ = "ChallengeClasses"

    name = Column(String, primary_key=True)
    class_name = Column(String, nullable=False, name="class")
    comparison_operator = Column(String, nullable=False)


class Games(Base):
    __tablename__ = "Games"

    match_id = Column(String, primary_key=True)
    summoner_id = Column(String, ForeignKey("summoners.puuid"), nullable=False, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    win = Column(Boolean, nullable=False)
    lane = Column(String, nullable=False)
    stats = Column(String, nullable=False)
    challenges = Column(String, nullable=False)

    summoner = relationship("Summoners", foreign_keys=[summoner_id])


Base.metadata.create_all(engine)
