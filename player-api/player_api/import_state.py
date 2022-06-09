import os

import grpc
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from player_api.log import get_logger
from player_api.models.player import PlayerId
from player_api.get_player import get_player_by_id
from player_api.models.player import ImportProgress, ImportState
from player_api.playerImportRequest_pb2 import ImportRequest, ImportReply
from player_api.playerImportRequest_pb2_grpc import ImporterStub

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
    with grpc.insecure_channel(
        f"{os.environ.get('GRPC_IMPORT_HOST', 'localhost')}:50051"
    ) as channel:
        stub = ImporterStub(channel)
        try:
            for value in stub.import_player(ImportRequest(puuid=player_id)):
                global_import_state.set_import_state(
                    player_id,
                    progress=ImportProgress(
                        imported_games=value.games_imported,
                        total_games=value.total_games,
                        imported=False,
                        percentage=ImportProgress.calc_percentage(
                            value.games_imported, value.total_games
                        ),
                        import_state=ImportState.IMPORTING,
                    ),
                )
                logger.debug(
                    f"method=import_player_task {global_import_state.of(player_id)=}"
                )
            global_import_state.set_import_state(
                player_id,
                progress=ImportProgress(
                    imported_games=0,
                    total_games=0,
                    imported=True,
                    percentage=1,
                    import_state=ImportState.FINISHED,
                ),
            )
            logger.debug(
                f"method=import_player_task msg='finished importing' {global_import_state.of(player_id)=}"
            )
        except Exception as e:
            global_import_state.set_import_state(
                player_id,
                progress=ImportProgress(
                    imported_games=0,
                    total_games=0,
                    imported=False,
                    percentage=0,
                    import_state=ImportState.FAILED,
                ),
            )
            logger.warning(
                f"method=import_player_task msg='FAILED importing' {global_import_state.of(player_id)=} exception={e}"
            )


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
        return player_id in self.players and self.players[player_id].import_state in [
            ImportState.IMPORTING,
            ImportState.PENDING,
        ]

    def set_import_state(self, player_id: PlayerId, progress: ImportProgress):
        self.players[player_id] = progress


global_import_state = GlobalImportState()
