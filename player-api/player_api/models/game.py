from datetime import datetime
from enum import Enum
from typing import TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")


class Page(GenericModel, Generic[T]):
    items: list[T]
    next: str


class TeamSide(str, Enum):
    red = "red"
    blue = "blue"


class Champion(BaseModel):
    name: str
    icon_path: str


class GamePlayer(BaseModel):
    id: str
    name: str


class PlayerStats(BaseModel):
    kills: int
    deaths: int
    assists: int
    creep_score: int


class TeamMember(BaseModel):
    champion: Champion
    player: GamePlayer
    stats: PlayerStats
    team: TeamSide
    lane: str


class Game(BaseModel):
    match_id: str
    victorious_team: TeamSide
    ally_team: list[TeamMember]
    enemy_team: list[TeamMember]
    self: TeamMember
    win: bool
    duration: int
    timestamp: datetime
