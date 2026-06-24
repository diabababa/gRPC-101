"""Solution: Locust load test for gRPC Chat service."""

import time

import grpc
from locust import User, between, events, task

from solutions.generated import chat_pb2, chat_pb2_grpc

HOST = "localhost:50051"


class GrpcUser(User):
    abstract = True

    def on_start(self):
        self._channel = grpc.insecure_channel(HOST)
        self._stub = chat_pb2_grpc.ChatServiceStub(self._channel)

    def on_stop(self):
        self._channel.close()

    def _call(self, name, func, *args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            events.request.fire(
                request_type="grpc", name=name,
                response_time=elapsed_ms, response_length=0,
            )
            return result
        except grpc.RpcError as exc:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            events.request.fire(
                request_type="grpc", name=name,
                response_time=elapsed_ms, response_length=0, exception=exc,
            )
            raise


class ChatUser(GrpcUser):
    wait_time = between(0.5, 2)

    @task(3)
    def send_message(self):
        self._call(
            "SendMessage",
            self._stub.SendMessage,
            chat_pb2.MessageRequest(
                room_id="perf-room", user="locust", content="Load test message"
            ),
        )

    @task(1)
    def get_history(self):
        self._call(
            "GetHistory",
            lambda req: list(self._stub.GetHistory(req)),
            chat_pb2.HistoryRequest(room_id="perf-room", limit=5),
        )

    @task(1)
    def send_bulk(self):
        def _reqs():
            for i in range(5):
                yield chat_pb2.MessageRequest(
                    room_id="perf-room", user="locust-bulk", content=f"bulk {i}"
                )

        self._call("SendBulkMessages", self._stub.SendBulkMessages, _reqs())
