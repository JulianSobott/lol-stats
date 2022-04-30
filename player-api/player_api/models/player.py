from enum import Enum

from pydantic import BaseModel, Field


class RankEnum(str, Enum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"
    V = "V"


class TierEnum(str, Enum):
    IRON = "IRON"
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATIN = "PLATIN"
    DIAMOND = "DIAMOND"
    MASTER = "MASTER"
    CHALLENGER = "CHALLENGER"


class Rank(BaseModel):
    rank: RankEnum
    tier: TierEnum
    league_points: int = Field(ge=0, le=100)


class MostPlayed(BaseModel):
    champion_id: int
    rank: int


class Player(BaseModel):
    id: str
    icon_path: str
    name: str
    win_rate: float = Field(ge=0, le=100)
    rank: Rank
    most_played: list[MostPlayed]
