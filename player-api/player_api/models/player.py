from enum import Enum

from pydantic import BaseModel, Field


class TierEnum(str, Enum):
    IRON = "IRON"
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"
    DIAMOND = "DIAMOND"
    MASTER = "MASTER"
    GRANDMASTER = "GRANDMASTER"
    CHALLENGER = "CHALLENGER"


class Rank(BaseModel):
    rank: int = Field(ge=1, le=5)
    tier: TierEnum
    league_points: int = Field(ge=0, le=100)


class MostPlayed(BaseModel):
    champion_id: int
    champion_name: str
    icon_path: str
    games: int
    win_rate: int = Field(ge=0, le=100)


class Player(BaseModel):
    id: str
    player_icon_path: str
    name: str
    win_rate: int = Field(ge=0, le=100)
    level: int
    rank: Rank
    most_played: list[MostPlayed]
