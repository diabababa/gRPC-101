"""Exercise 3 — experiment with all four gRPC streaming patterns.

Run the reference server first:
    poe server

Then run this script:
    python exercises/03_streaming/streaming_starter.py
"""

import grpc

from chat.generated import chat_pb2, chat_pb2_grpc

CHANNEL = "localhost:50051"


def demo_unary(stub: chat_pb2_grpc.ChatServiceStub) -> None:
    """Already working — just run it."""
    resp = stub.SendMessage(
        chat_pb2.MessageRequest(room_id="demo", user="alice", content="Hello!")
    )
    print(f"[Unary] Sent: id={resp.message_id}")


def demo_server_streaming(stub: chat_pb2_grpc.ChatServiceStub) -> None:
    """TODO: call GetHistory and print each message."""
    print("\n[Server streaming] GetHistory:")

    # First send a few messages so there is something to fetch
    for i in range(3):
        stub.SendMessage(
            chat_pb2.MessageRequest(room_id="demo", user="alice", content=f"msg {i}")
        )

    # TODO: call stub.GetHistory with a HistoryRequest
    # TODO: iterate the result and print each message


def demo_client_streaming(stub: chat_pb2_grpc.ChatServiceStub) -> None:
    """TODO: send 5 messages in a single client-streaming call."""
    print("\n[Client streaming] SendBulkMessages:")

    # TODO: define a generator that yields 5 MessageRequests
    def messages():
        for i in range(5):
            yield chat_pb2.MessageRequest(
                room_id="bulk",
                user="alice",
                content=f"bulk message {i}",
            )

    # TODO: call stub.SendBulkMessages(messages()) and print the result


def demo_bidirectional(stub: chat_pb2_grpc.ChatServiceStub) -> None:
    """TODO: send 3 messages via Chat and print the echoed responses."""
    print("\n[Bidirectional] Chat:")

    inputs = ["Hi there!", "How does gRPC work?", "Thanks, goodbye!"]

    # TODO: define a generator for the inputs
    def requests():
        for text in inputs:
            yield chat_pb2.MessageRequest(room_id="bidi", user="alice", content=text)

    # TODO: call stub.Chat(requests()) and iterate the responses


def main():
    with grpc.insecure_channel(CHANNEL) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        demo_unary(stub)
        demo_server_streaming(stub)
        demo_client_streaming(stub)
        demo_bidirectional(stub)


if __name__ == "__main__":
    main()
