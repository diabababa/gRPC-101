"""Exercise 3 — implement the unary SendMessage RPC."""

import time
import uuid
from concurrent import futures

import grpc

from exercises.generated import chat_pb2, chat_pb2_grpc

_store: dict[str, list] = {}


def _make_message(request: chat_pb2.MessageRequest) -> chat_pb2.Message:
    """Save request to the in-memory store and return a Message proto."""
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
        # TODO 1: validate — abort with INVALID_ARGUMENT if request.content is empty
        # hint: context.abort(grpc.StatusCode.INVALID_ARGUMENT, "reason")

        # TODO 2: save — call _make_message(request) and store the result
        msg = ...

        # TODO 3: return a MessageResponse with message_id, status="ok", timestamp
        return chat_pb2.MessageResponse(
            message_id=...,
            status=...,
            timestamp=...,
        )

    # The other methods are not needed yet — leave them as-is.
    def GetHistory(self, request, context):
        pass

    def SendBulkMessages(self, request_iterator, context):
        pass

    def Chat(self, request_iterator, context):
        pass


def serve(port: int = 50051) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server listening on :{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
