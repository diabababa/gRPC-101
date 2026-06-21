"""Exercise 2 — implement a basic unary gRPC client."""

import grpc

from chat.generated import chat_pb2, chat_pb2_grpc


def main():
    # TODO: create an insecure channel to localhost:50051
    channel = ...

    # TODO: create a stub (use chat_pb2_grpc.ChatServiceStub)
    stub = ...

    # TODO: call stub.SendMessage with a MessageRequest
    #   Fields: room_id="general", user="alice", content="Hello EuroPython!"
    response = stub.SendMessage(
        chat_pb2.MessageRequest(
            # TODO: fill in fields
        )
    )

    # TODO: print the message_id and status from the response
    print(f"message_id: {response.message_id}")
    print(f"status:     {response.status}")

    # Don't forget to close the channel!
    channel.close()


if __name__ == "__main__":
    main()
