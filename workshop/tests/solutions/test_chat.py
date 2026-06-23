import time
from concurrent.futures import ThreadPoolExecutor

import grpc
import pytest

from chat.generated import chat_pb2, chat_pb2_grpc


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


# ---------------------------------------------------------------------------
# Protocol Buffers — generated schema (Exercise 01)
# ---------------------------------------------------------------------------

def test_message_content_is_preserved(stub):
    resp = _send(stub, room="content-room", content="preserved text")
    assert resp.status == "ok"
    messages = list(stub.GetHistory(chat_pb2.HistoryRequest(room_id="content-room", limit=1)))
    assert messages[0].content == "preserved text"


# ---------------------------------------------------------------------------
# Protocol Buffers — generated schema (Exercise 01)
# ---------------------------------------------------------------------------

def test_proto_message_types_have_correct_fields():
    msg = chat_pb2.MessageRequest(room_id="r", user="u", content="c")
    assert msg.room_id == "r" and msg.user == "u" and msg.content == "c"

    resp = chat_pb2.MessageResponse(message_id="id", status="ok", timestamp=1)
    assert resp.message_id == "id" and resp.status == "ok"

    hist = chat_pb2.HistoryRequest(room_id="room", limit=5)
    assert hist.room_id == "room" and hist.limit == 5

    stored = chat_pb2.Message(
        message_id="id", room_id="r", user="u", content="c", timestamp=1
    )
    assert stored.content == "c"


def test_proto_stub_has_all_four_rpc_methods(stub):
    for method in ("SendMessage", "GetHistory", "SendBulkMessages", "Chat"):
        assert hasattr(stub, method)


# ---------------------------------------------------------------------------
# Performance (Exercise 05)
# ---------------------------------------------------------------------------

def test_service_handles_concurrent_requests(grpc_addr):
    errors = []

    def _send(i):
        try:
            with grpc.insecure_channel(grpc_addr) as ch:
                s = chat_pb2_grpc.ChatServiceStub(ch)
                s.SendMessage(
                    chat_pb2.MessageRequest(room_id="perf-sol", user="bot", content=f"msg {i}")
                )
        except grpc.RpcError as e:
            errors.append(e)

    with ThreadPoolExecutor(max_workers=10) as pool:
        list(pool.map(_send, range(50)))

    assert len(errors) == 0


def test_service_responds_within_time_limit(stub):
    t0 = time.perf_counter()
    for i in range(30):
        stub.SendMessage(
            chat_pb2.MessageRequest(room_id="perf-seq-sol", user="bot", content=f"seq {i}")
        )
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert elapsed_ms < 500 * 30
