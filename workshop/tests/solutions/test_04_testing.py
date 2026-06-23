"""Solution tests — Exercise 04: Writing Tests.

This is the reference solution showing what good pytest tests for the chat service look like.
"""
import pytest
import grpc

from chat.generated import chat_pb2


def _send(stub, room="test-room", user="alice", content="Hi!"):
    return stub.SendMessage(
        chat_pb2.MessageRequest(room_id=room, user=user, content=content)
    )


def test_send_message_returns_id_and_ok_status(stub):
    resp = _send(stub)
    assert resp.message_id != ""
    assert resp.status == "ok"
    assert resp.timestamp > 0


def test_send_message_generates_unique_ids(stub):
    id1 = _send(stub, room="t4-unique").message_id
    id2 = _send(stub, room="t4-unique").message_id
    assert id1 != id2


def test_empty_content_raises_invalid_argument(stub):
    with pytest.raises(grpc.RpcError) as exc_info:
        stub.SendMessage(
            chat_pb2.MessageRequest(room_id="room", user="alice", content="")
        )
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_get_history_returns_sent_messages(stub):
    room = "t4-history"
    for i in range(3):
        _send(stub, room=room, content=f"msg {i}")
    messages = list(stub.GetHistory(chat_pb2.HistoryRequest(room_id=room, limit=10)))
    assert len(messages) == 3


def test_send_bulk_messages(stub):
    def _requests():
        for i in range(5):
            yield chat_pb2.MessageRequest(
                room_id="t4-bulk", user="alice", content=f"bulk {i}"
            )

    resp = stub.SendBulkMessages(_requests())
    assert resp.messages_sent == 5
    assert resp.messages_failed == 0
