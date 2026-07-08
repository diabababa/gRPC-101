from concurrent import futures

import grpc
import pytest

from solutions.server import ChatServicer
from solutions.generated import chat_pb2_grpc


@pytest.fixture(scope="session")
def grpc_addr():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    port = server.add_insecure_port("[::]:0")
    server.start()
    yield f"localhost:{port}"
    server.stop(grace=None)


@pytest.fixture
def stub(grpc_addr):
    with grpc.insecure_channel(grpc_addr) as channel:
        yield chat_pb2_grpc.ChatServiceStub(channel)
