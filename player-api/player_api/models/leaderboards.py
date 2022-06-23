from pydantic import BaseModel


class LeaderboardPlayer(BaseModel):
    id: str
    name: str
    player_icon_path: str
    value: float


class Challenge(BaseModel):
    name: str
    players: list[LeaderboardPlayer]


class Leaderboards(BaseModel):
    challenges: list[Challenge]
