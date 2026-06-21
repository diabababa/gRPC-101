import time
import uuid
from concurrent import futures

import grpc
from prometheus_client import Counter, Histogram, start_http_server

from chat.generated import chat_pb2, chat_pb2_grpc

# In-memory message store: room_id → list[Message]
_store: dict[str, list[chat_pb2.Message]] = {}

REQUEST_COUNT = Counter(
    "grpc_requests_total",
    "Total gRPC requests",
    ["method", "status"],
)
REQUEST_LATENCY = Histogram(
    "grpc_request_duration_seconds",
    "gRPC request duration in seconds",
    ["method"],
)


def _make_message(request: chat_pb2.MessageRequest) -> chat_pb2.Message:
    msg = chat_pb2.Message(
        message_id=str(uuid.uuid4()),
        room_id=request.room_id,
        user=request.user,
        content=request.content,
        timestamp=int(time.time()),
    )
    _store.setdefault(request.room_id, []).append(msg)
    return msg


class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def SendMessage(self, request, context):
        if not request.content.strip():
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Message content cannot be empty",
            )

        with REQUEST_LATENCY.labels(method="SendMessage").time():
            msg = _make_message(request)

        REQUEST_COUNT.labels(method="SendMessage", status="ok").inc()
        return chat_pb2.MessageResponse(
            message_id=msg.message_id,
            status="ok",
            timestamp=msg.timestamp,
        )

    def GetHistory(self, request, context):
        with REQUEST_LATENCY.labels(method="GetHistory").time():
            messages = _store.get(request.room_id, [])
            limit = request.limit if request.limit > 0 else len(messages)
            for msg in messages[-limit:]:
                yield msg

        REQUEST_COUNT.labels(method="GetHistory", status="ok").inc()

    def SendBulkMessages(self, request_iterator, context):
        sent = failed = 0
        with REQUEST_LATENCY.labels(method="SendBulkMessages").time():
            for request in request_iterator:
                try:
                    _make_message(request)
                    sent += 1
                except Exception:
                    failed += 1

        REQUEST_COUNT.labels(method="SendBulkMessages", status="ok").inc()
        return chat_pb2.BulkResponse(messages_sent=sent, messages_failed=failed)

    def Chat(self, request_iterator, context):
        REQUEST_COUNT.labels(method="Chat", status="ok").inc()
        with REQUEST_LATENCY.labels(method="Chat").time():
            for request in request_iterator:
                if context.is_active():
                    yield _make_message(request)


def serve(port: int = 50051, metrics_port: int = 8000) -> None:
    start_http_server(metrics_port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"gRPC server listening on :{port}")
    print(f"Prometheus metrics at http://localhost:{metrics_port}/metrics")
    server.wait_for_termination()
