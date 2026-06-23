"""Exercise 02 — First gRPC Service (unary).

Implement ChatServicer.SendMessage in chat/server.py, then make these tests pass.
Run: poe test-exercises
"""
import pytest
import grpc

from chat.generated import chat_pb2


def test_send_message_returns_non_empty_id(stub):
    # TODO: call stub.SendMessage with MessageRequest(room_id=..., user=..., content=...)
    # TODO: assert resp.message_id != ""
    pytest.fail("Implement this test")


def test_send_message_returns_ok_status(stub):
    # TODO: call stub.SendMessage
    # TODO: assert resp.status == "ok"
    pytest.fail("Implement this test")


def test_send_message_returns_positive_timestamp(stub):
    # TODO: call stub.SendMessage
    # TODO: assert resp.timestamp > 0
    pytest.fail("Implement this test")


def test_send_message_generates_unique_ids(stub):
    # TODO: send two messages to the same room
    # TODO: assert the message_ids are different
    pytest.fail("Implement this test")


def test_empty_content_raises_invalid_argument(stub):
    # TODO: use pytest.raises(grpc.RpcError) to catch the error
    # TODO: call stub.SendMessage with content=""
    # TODO: assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    pytest.fail("Implement this test")
