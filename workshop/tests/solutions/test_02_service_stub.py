"""Solution tests — Exercise 02: Service Stub."""

from solutions.generated import chat_pb2_grpc
from solutions.server import ChatServicer


def test_chatservicer_inherits_from_generated_base():
    assert issubclass(ChatServicer, chat_pb2_grpc.ChatServiceServicer)


def test_chatservicer_has_send_message():
    assert callable(getattr(ChatServicer, "SendMessage", None))


def test_chatservicer_has_get_history():
    assert callable(getattr(ChatServicer, "GetHistory", None))


def test_chatservicer_has_send_bulk_messages():
    assert callable(getattr(ChatServicer, "SendBulkMessages", None))


def test_chatservicer_has_chat():
    assert callable(getattr(ChatServicer, "Chat", None))


def test_chatservicer_can_be_instantiated():
    assert ChatServicer() is not None
