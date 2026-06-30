"""Exercise 2 — build a gRPC service stub (class structure only)."""

from concurrent import futures

import grpc

from exercises.generated import chat_pb2_grpc


# TODO: Create ChatServicer that inherits from chat_pb2_grpc.ChatServiceServicer
# Hint: open exercises/generated/chat_pb2_grpc.py and find ChatServiceServicer
class ChatServicer(...):  # replace ... with the correct base class

    # TODO: add SendMessage(self, request, context) — return pass for now
    pass

    # TODO: add GetHistory(self, request, context) — return pass for now

    # TODO: add SendBulkMessages(self, request_iterator, context) — return pass

    # TODO: add Chat(self, request_iterator, context) — return pass


def serve(port: int = 50051) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # TODO: register your servicer
    # hint: chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server listening on :{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
