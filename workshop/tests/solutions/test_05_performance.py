"""Solution tests — Exercise 05: Performance Testing."""
import time
from concurrent.futures import ThreadPoolExecutor

import grpc

from solutions.generated import chat_pb2, chat_pb2_grpc


def test_service_handles_concurrent_requests(grpc_addr):
    errors = []

    def _send(i):
        try:
            with grpc.insecure_channel(grpc_addr) as ch:
                s = chat_pb2_grpc.ChatServiceStub(ch)
                s.SendMessage(
                    chat_pb2.MessageRequest(
                        room_id="sol-perf", user="bot", content=f"msg {i}"
                    )
                )
        except grpc.RpcError as e:
            errors.append(e)

    with ThreadPoolExecutor(max_workers=10) as pool:
        list(pool.map(_send, range(50)))

    assert len(errors) == 0


def test_service_responds_within_time_limit(stub):
    t0 = time.perf_counter()
    for i in range(30):
        stub.SendMessage(
            chat_pb2.MessageRequest(
                room_id="sol-perf-seq", user="bot", content=f"seq {i}"
            )
        )
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert elapsed_ms < 500 * 30
