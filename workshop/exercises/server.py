import time
import uuid
from concurrent import futures

import grpc
from prometheus_client import Counter, Histogram, start_http_server

from exercises.generated import chat_pb2, chat_pb2_grpc

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
        # TODO Exercise 02 — implement unary RPC
        # 1. Validate request.content is not empty; abort with INVALID_ARGUMENT if so
        # 2. Call _make_message(request) to save and get a Message
        # 3. Return MessageResponse(message_id=..., status="ok", timestamp=...)
        pass

    def GetHistory(self, request, context):
        # TODO Exercise 03 — implement server streaming
        # 1. Look up _store.get(request.room_id, [])
        # 2. Apply request.limit (0 = all)
        # 3. yield each Message
        pass

    def SendBulkMessages(self, request_iterator, context):
        # TODO Exercise 03 — implement client streaming
        # 1. Iterate request_iterator
        # 2. Call _make_message for each request
        # 3. Return BulkResponse(messages_sent=..., messages_failed=...)
        pass

    def Chat(self, request_iterator, context):
        # TODO Exercise 03 (bonus) — bidirectional streaming
        # 1. Iterate request_iterator
        # 2. For each request, save and yield the message back
        pass


def serve(port: int = 50051, metrics_port: int = 8000) -> None:
    start_http_server(metrics_port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"gRPC server listening on :{port}")
    print(f"Prometheus metrics at http://localhost:{metrics_port}/metrics")
    server.wait_for_termination()
