"""Solution: unary gRPC server."""

import time
import uuid
from concurrent import futures

import grpc

from solutions.generated import chat_pb2, chat_pb2_grpc

_store: dict[str, list] = {}


class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def SendMessage(self, request, context):
        if request.content == "":
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Message content cannot be empty",
            )
        message_id = str(uuid.uuid4())
        timestamp = int(time.time())
        msg = chat_pb2.Message(
            message_id=message_id,
            room_id=request.room_id,
            user=request.user,
            content=request.content,
            timestamp=timestamp,
        )
        _store.setdefault(request.room_id, []).append(msg)
        return chat_pb2.MessageResponse(
            message_id=message_id,
            status="ok",
            timestamp=timestamp,
        )


def serve(port: int = 50051) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server listening on :{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
