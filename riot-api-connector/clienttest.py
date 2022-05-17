import os

import grpc
from playerImportRequest_pb2_grpc import ImporterStub
from playerImportRequest_pb2 import ImportRequest


def run():
    with grpc.insecure_channel(f"{os.environ.get('GRPC_IMPORT_HOST', 'localhost')}:50051") as channel:
        stub = ImporterStub(channel)
        for value in stub.import_player(ImportRequest(puuid="U1eAXj5kivutihmOfIxTusnMnSLRuRK7grTadgVNiks9rwh3Wye5eRTW3fd0Hm1eGFSBgnYiHfNz8Q")):
            print(f"{value.games_imported}/{value.total_games}")


if __name__ == '__main__':
    run()