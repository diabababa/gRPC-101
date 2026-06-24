"""Exercise 5 — Locust load test for the gRPC Chat service.

Run:
    locust -f exercises/05_performance/locustfile_starter.py
    # Open http://localhost:8089
"""

import time

import grpc
from locust import User, between, events, task

from exercises.generated import chat_pb2, chat_pb2_grpc

HOST = "localhost:50051"


class GrpcUser(User):
    """Base class — manages a gRPC channel per simulated user."""

    abstract = True

    def on_start(self):
        self._channel = grpc.insecure_channel(HOST)
        self._stub = chat_pb2_grpc.ChatServiceStub(self._channel)

    def on_stop(self):
        self._channel.close()

    def _call(self, name: str, func, *args, **kwargs):
        """Time a gRPC call and report it to Locust."""
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            events.request.fire(
                request_type="grpc",
                name=name,
                response_time=elapsed_ms,
                response_length=0,
            )
            return result
        except grpc.RpcError as exc:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            events.request.fire(
                request_type="grpc",
                name=name,
                response_time=elapsed_ms,
                response_length=0,
                exception=exc,
            )
            raise


class ChatUser(GrpcUser):
    wait_time = between(0.5, 2)

    @task(3)
    def send_message(self):
        # TODO: use self._call("SendMessage", self._stub.SendMessage, <MessageRequest>)
        pass

    @task(1)
    def get_history(self):
        # TODO: use self._call("GetHistory", lambda req: list(self._stub.GetHistory(req)), <HistoryRequest>)
        # hint: wrap in lambda so the iterator is consumed inside _call's timing window
        pass

    # BONUS
    @task(1)
    def send_bulk(self):
        def _reqs():
            for i in range(5):
                yield chat_pb2.MessageRequest(
                    room_id="perf-room",
                    user="locust-bulk",
                    content=f"bulk {i}",
                )

        # TODO: call _call("SendBulkMessages", self._stub.SendBulkMessages, _reqs())
        pass
