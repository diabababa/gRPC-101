"""Solution: all four gRPC communication patterns."""

import grpc

from chat.generated import chat_pb2, chat_pb2_grpc

CHANNEL = "localhost:50051"


def demo_unary(stub):
    resp = stub.SendMessage(
        chat_pb2.MessageRequest(room_id="demo", user="alice", content="Hello!")
    )
    print(f"[Unary] Sent: id={resp.message_id}")


def demo_server_streaming(stub):
    print("\n[Server streaming] GetHistory:")
    for i in range(3):
        stub.SendMessage(
            chat_pb2.MessageRequest(room_id="demo", user="alice", content=f"msg {i}")
        )
    for msg in stub.GetHistory(chat_pb2.HistoryRequest(room_id="demo", limit=10)):
        print(f"  [{msg.user}] {msg.content}")


def demo_client_streaming(stub):
    print("\n[Client streaming] SendBulkMessages:")

    def messages():
        for i in range(5):
            yield chat_pb2.MessageRequest(
                room_id="bulk", user="alice", content=f"bulk message {i}"
            )

    resp = stub.SendBulkMessages(messages())
    print(f"  Sent: {resp.messages_sent}  Failed: {resp.messages_failed}")


def demo_bidirectional(stub):
    print("\n[Bidirectional] Chat:")
    inputs = ["Hi there!", "How does gRPC work?", "Thanks, goodbye!"]

    def requests():
        for text in inputs:
            yield chat_pb2.MessageRequest(room_id="bidi", user="alice", content=text)

    for reply in stub.Chat(requests()):
        print(f"  ← [{reply.user}] {reply.content}")


def main():
    with grpc.insecure_channel(CHANNEL) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        demo_unary(stub)
        demo_server_streaming(stub)
        demo_client_streaming(stub)
        demo_bidirectional(stub)


if __name__ == "__main__":
    main()
