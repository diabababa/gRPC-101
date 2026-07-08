"""Solution: pytest tests for gRPC Chat service."""

import pytest
import grpc

from solutions.generated import chat_pb2


def _send(stub, room="test", user="alice", content="Hi!"):
    return stub.SendMessage(
        chat_pb2.MessageRequest(room_id=room, user=user, content=content)
    )


def test_send_message_returns_id(stub):
    resp = _send(stub)
    assert resp.message_id != ""
    assert resp.status == "ok"
    assert resp.timestamp > 0


def test_get_history_returns_messages(stub):
    room = "solution-history"
    for i in range(3):
        _send(stub, room=room, content=f"msg {i}")
    messages = list(
        stub.GetHistory(chat_pb2.HistoryRequest(room_id=room, limit=10))
    )
    assert len(messages) == 3


def test_empty_content_is_rejected(stub):
    with pytest.raises(grpc.RpcError) as exc_info:
        stub.SendMessage(
            chat_pb2.MessageRequest(room_id="room", user="alice", content="")
        )
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_send_bulk_messages(stub):
    def _requests():
        for i in range(5):
            yield chat_pb2.MessageRequest(
                room_id="solution-bulk", user="alice", content=f"bulk {i}"
            )

    resp = stub.SendBulkMessages(_requests())
    assert resp.messages_sent == 5
    assert resp.messages_failed == 0
