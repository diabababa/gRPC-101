"""Solution: service stub — class structure with method stubs."""

from concurrent import futures

import grpc

from solutions.generated import chat_pb2_grpc


class ChatServicer(chat_pb2_grpc.ChatServiceServicer):

    def SendMessage(self, request, context):
        pass

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
