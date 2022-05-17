from asyncio import futures
from playerImportRequest_pb2_grpc import ImporterServicer, add_ImporterServicer_to_server
from playerImportRequest_pb2 import ImportRequest, ImportReply
import grpc


class PlayerImportRequest(ImporterServicer):

    def __init__(self, addSummonerMethod) -> None:
        self.addSummoner = addSummonerMethod

    def import_player(self, request, context):
        for progress, total in self.addSummoner(id=request.puuid):
            yield ImportReply(games_imported=progress, total_games=total)



def serve(addSummonerMethod):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ImporterServicer_to_server(PlayerImportRequest(addSummonerMethod=addSummonerMethod), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
