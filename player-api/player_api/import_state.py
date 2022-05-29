from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from player_api.log import get_logger
from player_api.models.player import PlayerId
from player_api.get_player import get_player_by_id
from player_api.models.player import ImportProgress, ImportState


logger = get_logger(__name__)


def is_player_currently_imported(player_id: PlayerId) -> bool:
    return global_import_state.is_player_currently_imported(player_id)


def is_player_imported(db: Session, player_id: PlayerId) -> bool:
    player = get_player_by_id(db, player_id)
    return player is not None and player.last_update is not None


def get_import_progress(player_id: PlayerId) -> ImportProgress:
    return global_import_state.of(player_id)


def start_import(
    player_id: PlayerId, background_tasks: BackgroundTasks
) -> ImportProgress:
    global_import_state.set_import_state(
        player_id,
        ImportProgress(
            imported_games=0,
            total_games=0,
            imported=False,
            import_state=ImportState.PENDING,
            percentage=ImportProgress.calc_percentage(0, 0),
        ),
    )
    background_tasks.add_task(import_player_task, player_id)
    return global_import_state.of(player_id)


def import_player_task(player_id: PlayerId):
    pass


class GlobalImportState:
    def __init__(self):
        self.players: dict[PlayerId, ImportProgress] = {}

    def of(self, player_id: PlayerId) -> ImportProgress:
        if player_id not in self.players:
            logger.warning(
                f"Trying to get ImportState of player that is not currently imported. {player_id=}"
            )
            return ImportProgress(
                imported_games=0,
                total_games=0,
                import_state=ImportState.PENDING,
                imported=False,
                percentage=ImportProgress.calc_percentage(0, 0),
            )
        return self.players[player_id]

    def is_player_currently_imported(self, player_id: PlayerId):
        return player_id in self.players

    def set_import_state(self, player_id: PlayerId, progress: ImportProgress):
        self.players[player_id] = progress


global_import_state = GlobalImportState()
