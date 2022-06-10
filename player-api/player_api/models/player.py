from enum import Enum

from pydantic import BaseModel, Field


class TierEnum(str, Enum):
    IRON = "iron"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"
    MASTER = "master"
    GRANDMASTER = "grandmaster"
    CHALLENGER = "challenger"
    UNRANKED = "unranked"


class Rank(BaseModel):
    division: int = Field(ge=1, le=4)
    tier: TierEnum
    league_points: int = Field(ge=0, le=100)

    @property
    def division_str(self) -> str:
        return {
            1: "I",
            2: "II",
            3: "III",
            4: "IV",
        }[self.division]

    @staticmethod
    def division_from_str(division: str) -> int:
        return {"I": 1, "II": 2, "III": 3, "IV": 4}[division]


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


PlayerId = str
PlayerName = str
UserId = str
