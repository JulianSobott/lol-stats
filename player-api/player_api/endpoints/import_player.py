from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from player_api.import_state import (
    is_player_currently_imported,
    get_import_progress,
    is_player_imported,
    start_import,
)
from player_api.log import get_logger
from player_api.middlewares import get_db
from player_api.models.player import ImportProgress, PlayerId, ImportState
from player_api.models.responses import ExceptionMessage

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/players/{player_id}/import",
    response_model=ImportProgress,
    responses={404: {"model": ExceptionMessage, "description": "Player not found"}},
)
async def import_player(
    player_id: PlayerId,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if is_player_currently_imported(player_id):
        return get_import_progress(player_id)
    if is_player_imported(db, player_id):
        return ImportProgress(
            imported=True,
            imported_games=0,
            total_games=0,
            percentage=100,
            import_state=ImportState.FINISHED,
        )
    return start_import(player_id, background_tasks)
