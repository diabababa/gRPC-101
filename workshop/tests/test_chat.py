import pytest
import grpc

from chat.generated import chat_pb2


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _send(stub, room: str = "test-room", user: str = "alice", content: str = "Hi!"):
    return stub.SendMessage(
        chat_pb2.MessageRequest(room_id=room, user=user, content=content)
    )


# ---------------------------------------------------------------------------
# Unary — SendMessage
# ---------------------------------------------------------------------------

def test_send_message_returns_id_and_ok_status(stub):
    resp = _send(stub)
    assert resp.message_id != ""
    assert resp.status == "ok"
    assert resp.timestamp > 0


def test_send_message_generates_unique_ids(stub):
    id1 = _send(stub, room="unique-room").message_id
    id2 = _send(stub, room="unique-room").message_id
    assert id1 != id2


def test_send_empty_content_raises_invalid_argument(stub):
    with pytest.raises(grpc.RpcError) as exc_info:
        stub.SendMessage(
            chat_pb2.MessageRequest(room_id="room", user="alice", content="")
        )
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


# ---------------------------------------------------------------------------
# Server streaming — GetHistory
# ---------------------------------------------------------------------------

def test_get_history_returns_sent_messages(stub):
    room = "history-room-1"
    for i in range(3):
        _send(stub, room=room, content=f"msg {i}")

    messages = list(
        stub.GetHistory(chat_pb2.HistoryRequest(room_id=room, limit=10))
    )
    assert len(messages) == 3
    assert messages[0].content == "msg 0"
    assert messages[2].content == "msg 2"


def test_get_history_respects_limit(stub):
    room = "history-room-2"
    for i in range(5):
        _send(stub, room=room, content=f"msg {i}")

    messages = list(
        stub.GetHistory(chat_pb2.HistoryRequest(room_id=room, limit=2))
    )
    assert len(messages) == 2
    assert messages[0].content == "msg 3"  # last 2
    assert messages[1].content == "msg 4"


def test_get_history_empty_room_returns_nothing(stub):
    messages = list(
        stub.GetHistory(chat_pb2.HistoryRequest(room_id="empty-room", limit=10))
    )
    assert messages == []


# ---------------------------------------------------------------------------
# Client streaming — SendBulkMessages
# ---------------------------------------------------------------------------

def test_send_bulk_messages_returns_correct_count(stub):
    def _requests():
        for i in range(5):
            yield chat_pb2.MessageRequest(
                room_id="bulk-room", user="alice", content=f"bulk {i}"
            )

    resp = stub.SendBulkMessages(_requests())
    assert resp.messages_sent == 5
    assert resp.messages_failed == 0


# ---------------------------------------------------------------------------
# Bidirectional streaming — Chat
# ---------------------------------------------------------------------------

def test_chat_echoes_messages_back(stub):
    inputs = ["Hello", "How are you?", "Goodbye"]

    def _requests():
        for text in inputs:
            yield chat_pb2.MessageRequest(
                room_id="bidi-room", user="alice", content=text
            )

    replies = list(stub.Chat(_requests()))
    assert len(replies) == 3
    assert [r.content for r in replies] == inputs
