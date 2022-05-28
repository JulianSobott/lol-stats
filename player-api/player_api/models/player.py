from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator, root_validator


class TierEnum(str, Enum):
    iron = "iron"
    bronze = "bronze"
    silver = "silver"
    gold = "gold"
    platinum = "platinum"
    diamond = "diamond"
    master = "master"
    grandmaster = "grandmaster"
    challenger = "challenger"


class Rank(BaseModel):
    division: int = Field(ge=1, le=4)
    tier: TierEnum
    league_points: int = Field(ge=0, le=100)

    @property
    def division_str(self) -> str:
        return {
            1: "one",
            2: "two",
            3: "three",
            4: "four",
        }[self.division]

    @staticmethod
    def division_from_str(division: str) -> int:
        return {"one": 1, "two": 2, "three": 3, "four": 4}[division]


class MostPlayed(BaseModel):
    champion_id: int
    champion_name: str
    icon_path: str
    games: int
    win_rate: int = Field(ge=0, le=100)


class Player(BaseModel):
    """
    Optional fields are only None, when player is not imported yet, but exists.
    """

    id: str
    player_icon_path: str
    name: str
    win_rate: int | None = Field(ge=0, le=100)
    level: int
    rank: Rank | None
    most_played: list[MostPlayed] | None
    imported: bool


class BasicPlayer(BaseModel):
    id: str
    player_icon_path: str
    name: str
    level: int
    rank: Rank | None
    imported: bool


class ImportState(str, Enum):
    PENDING = "PENDING"  # client has to send a new request, to get more information
    IMPORTING = (
        "IMPORTING"  # client has to send a new request, to get the latest information
    )
    FINISHED = "FINISHED"  # client should send no new request
    FAILED = "FAILED"  # client may send a new request after some time to try again


class ImportProgress(BaseModel):
    imported_games: int
    total_games: int
    imported: bool
    import_state: ImportState
    percentage: int

    @staticmethod
    def calc_percentage(imported_games: int, total_games: int):
        if total_games == 0:
            return 100
        return int((imported_games / total_games) * 100)
