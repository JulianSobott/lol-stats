from enum import Enum

from pydantic import BaseModel


class Comparison(str, Enum):
    BETTER = "BETTER"
    EQUAL = "EQUAL"
    WORSE = "WORSE"


class AchievementStat(BaseModel):
    value: float
    compare: Comparison


class AchievementStats(BaseModel):
    max: AchievementStat
    total: AchievementStat
    avg: AchievementStat


class Achievement(BaseModel):
    fav: bool
    name: str
    description: str
    you: AchievementStats
    other: AchievementStats


class AchievementCategory(BaseModel):
    category: str
    achievements: list[Achievement]


class Achievements(BaseModel):
    items: list[AchievementCategory]
