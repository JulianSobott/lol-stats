from datetime import datetime
from enum import Enum
from typing import TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")


class Page(GenericModel, Generic[T]):
    items: list[T]
    next: str


class TeamSide(Enum):
    red = "red"
    blue = "blue"


class Champion(BaseModel):
    name: str
    icon_path: str


class GamePlayer(BaseModel):
    id: str
    name: str


class NameValue(BaseModel):
    name: str
    value: float | int


class TeamMember(BaseModel):
    champion: Champion
    player: GamePlayer
    player_stats: list[NameValue]


class Game(BaseModel):
    match_id: str
    victorious_team: TeamSide
    ally_team: list[TeamMember]
    enemy_team: list[TeamMember]
    duration: int
    timestamp: datetime
