"""Solution tests — Exercise 01: Protocol Buffers."""

from solutions.generated import chat_pb2, chat_pb2_grpc


def test_message_request_has_correct_fields():
    msg = chat_pb2.MessageRequest(room_id="r", user="u", content="c")
    assert msg.room_id == "r"
    assert msg.user == "u"
    assert msg.content == "c"


def test_message_response_has_correct_fields():
    resp = chat_pb2.MessageResponse(message_id="id", status="ok", timestamp=1)
    assert resp.message_id == "id"
    assert resp.status == "ok"
    assert resp.timestamp == 1


def test_history_request_has_correct_fields():
    req = chat_pb2.HistoryRequest(room_id="room", limit=5)
    assert req.room_id == "room"
    assert req.limit == 5


def test_message_has_all_five_fields():
    msg = chat_pb2.Message(
        message_id="id", room_id="r", user="u", content="c", timestamp=1
    )
    assert msg.message_id == "id"
    assert msg.room_id == "r"
    assert msg.user == "u"
    assert msg.content == "c"
    assert msg.timestamp == 1


def test_stub_has_all_four_rpc_methods(stub):
    for method in ("SendMessage", "GetHistory", "SendBulkMessages", "Chat"):
        assert hasattr(stub, method)
