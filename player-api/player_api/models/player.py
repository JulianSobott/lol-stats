from enum import Enum

from pydantic import BaseModel, Field, validator


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
    id: str
    player_icon_path: str
    name: str
    win_rate: int = Field(ge=0, le=100)
    level: int
    rank: Rank
    most_played: list[MostPlayed]


class BasicPlayer(BaseModel):
    id: str
    player_icon_path: str
    name: str
    level: int
    rank: Rank


class ImportProgress(BaseModel):
    imported_games: int
    total_games: int
    percentage: int

    @validator("percentage", always=True)
    def validate_percentage(cls, value, values):
        if values["total_games"] == 0:
            return 100
        percentage = int((values["imported_games"] / values["total_games"]) * 100)
        assert (
            0 <= percentage <= 100
        ), f"percentage not between 0 and 100: percentage={percentage}"
        return percentage
