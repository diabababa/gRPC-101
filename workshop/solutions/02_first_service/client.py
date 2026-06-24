"""Solution: unary gRPC client."""

import grpc

from solutions.generated import chat_pb2, chat_pb2_grpc


def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        response = stub.SendMessage(
            chat_pb2.MessageRequest(
                room_id="general",
                user="alice",
                content="Hello EuroPython!",
            )
        )
        print(f"message_id: {response.message_id}")
        print(f"status:     {response.status}")


if __name__ == "__main__":
    main()
