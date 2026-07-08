"""Solution tests — Exercise 04: Unary Client + Communication."""

import grpc
import pytest

from solutions.generated import chat_pb2


def _send(stub, room="client-test", user="alice", content="Hello!"):
    return stub.SendMessage(
        chat_pb2.MessageRequest(room_id=room, user=user, content=content)
    )


def test_client_can_send_message_and_receive_response(stub):
    resp = _send(stub)
    assert resp.message_id != ""
    assert resp.status == "ok"


def test_client_receives_unique_id_per_message(stub):
    id1 = _send(stub, room="unique-client").message_id
    id2 = _send(stub, room="unique-client").message_id
    assert id1 != id2


def test_client_gets_invalid_argument_on_empty_content(stub):
    with pytest.raises(grpc.RpcError) as exc_info:
        stub.SendMessage(
            chat_pb2.MessageRequest(room_id="room", user="alice", content="")
        )
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
