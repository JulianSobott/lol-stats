from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from player_api.get_player import get_player_by_name
from player_api.import_state import is_player_currently_imported, is_player_imported
from player_api.middlewares import get_db
from player_api.riot_api import find_player_in_riot_api_by, SearchTerm
from player_api.models.player import BasicPlayer, Rank
from player_api.models.responses import ExceptionMessage


router = APIRouter()


@router.get(
    "/players",
    response_model=BasicPlayer,
    responses={404: {"model": ExceptionMessage, "description": "Player not found"}},
)
def find_player(player_name: str, region: str = None, db: Session = Depends(get_db)):
    player = get_player_by_name(db, player_name)
    if player:
        if player.last_update is not None:
            if is_player_currently_imported(player.puuid):
                imported = False
            else:
                imported = True
            return BasicPlayer(
                id=player.puuid,
                player_icon_path=player.icon_path,
                name=player.name,
                level=player.level,
                rank=Rank(
                    division=Rank.division_from_str(player.division),
                    tier=player.tier,
                    league_points=player.league_points,
                ),
                imported=imported,
            )
        else:
            # player in database, but not imported
            return BasicPlayer(
                id=player.puuid,
                player_icon_path="",
                name=player.name,
                level=0,
                rank=None,
                imported=False,
            )
    player = find_player_in_riot_api_by(player_name, SearchTerm.name)
    if player:
        return player
    raise HTTPException(status_code=404, detail="player not found")
