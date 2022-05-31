import os

import grpc
from playerImportRequest_pb2_grpc import ImporterStub
from playerImportRequest_pb2 import ImportRequest


def run():
    with grpc.insecure_channel(f"{os.environ.get('GRPC_IMPORT_HOST', 'localhost')}:50051") as channel:
        stub = ImporterStub(channel)
        for value in stub.import_player(ImportRequest(puuid="iXhA-0-4teidjA09X9X5zyKtuIc8fSxJWvUsRhs6nhLlYJpNp63nyyjzpkI7X0Ou-wNyyxSCxJZ5Wg")):
            print(f"{value.games_imported}/{value.total_games}")


if __name__ == '__main__':
    run()
