"""Exercise 2 — implement a basic unary gRPC server."""

import time
import uuid
from concurrent import futures

import grpc

# Make sure you ran: poe generate
from chat.generated import chat_pb2, chat_pb2_grpc

# In-memory store: room_id → list of Message objects
_store: dict[str, list] = {}


# TODO: implement ChatServicer
# Inherit from chat_pb2_grpc.ChatServiceServicer
class ChatServicer(chat_pb2_grpc.ChatServiceServicer):

    def SendMessage(self, request, context):
        # TODO: validate request.content is not empty
        #   hint: context.abort(grpc.StatusCode.INVALID_ARGUMENT, "reason")

        # TODO: generate a UUID for message_id
        message_id = ...

        # TODO: record the timestamp
        timestamp = ...

        # TODO: save the message to _store
        #   hint: _store.setdefault(request.room_id, []).append(...)

        # TODO: return MessageResponse
        return chat_pb2.MessageResponse(
            message_id=message_id,
            status="ok",
            timestamp=timestamp,
        )


def serve(port: int = 50051) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # TODO: register your servicer with the server
    # hint: chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server listening on :{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
