from sqlalchemy.orm import Session

from player_api.db import Summoners


def get_player_by_id(db: Session, player_id: str) -> Summoners | None:
    player: Summoners | None = (
        db.query(Summoners).where(Summoners.puuid == player_id).first()
    )
    return player


def get_player_by_name(db: Session, player_name: str) -> Summoners | None:
    player: Summoners | None = (
        db.query(Summoners).where(Summoners.name == player_name).first()
    )
    return player
