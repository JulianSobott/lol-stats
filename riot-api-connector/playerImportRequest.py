from concurrent import futures
from playerImportRequest_pb2_grpc import ImporterServicer, add_ImporterServicer_to_server
from playerImportRequest_pb2 import ImportRequest, ImportReply
import grpc


class PlayerImportRequest(ImporterServicer):

    def __init__(self, db, addSummonerMethod) -> None:
        super(PlayerImportRequest, self).__init__()
        self.db = db
        self.addSummoner = addSummonerMethod

    def import_player(self, request, context):
        for progress, total in self.addSummoner(db=self.db, puuid=request.puuid):
            yield ImportReply(games_imported=progress, total_games=total)


def serve(db, addSummonerMethod):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ImporterServicer_to_server(PlayerImportRequest(db=db,
                                                       addSummonerMethod=addSummonerMethod), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
