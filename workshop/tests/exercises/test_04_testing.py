"""Exercise 04 — Writing Tests (TDD).

Write pytest tests from scratch. Tests start RED (server not implemented).
After you implement chat/server.py, make them GREEN.
Run: poe test-exercises
"""
import pytest
import grpc

from exercises.generated import chat_pb2


# ---------------------------------------------------------------------------
# Task 1: Test SendMessage (unary)
# ---------------------------------------------------------------------------

def test_send_message_returns_id(stub):
    """SendMessage should return a non-empty message_id and status 'ok'."""
    response = stub.SendMessage(
        chat_pb2.MessageRequest(
            # TODO: fill in room_id, user, content
        )
    )
    # TODO: assert response.message_id != ""
    # TODO: assert response.status == "ok"
    # TODO: assert response.timestamp > 0
    pytest.fail("Implement this test")


def test_send_message_generates_unique_ids(stub):
    """Two messages sent to the same room should have different message_ids."""
    # TODO: send two messages to the same room
    # TODO: assert the two message_ids are different
    pytest.fail("Implement this test")


# ---------------------------------------------------------------------------
# Task 2: Test GetHistory (server streaming)
# ---------------------------------------------------------------------------

def test_get_history_returns_messages(stub):
    """After sending 3 messages, GetHistory should stream all 3 back."""
    room = "exercise-history"
    # TODO: send 3 messages to room using stub.SendMessage in a loop
    # TODO: call stub.GetHistory(HistoryRequest(room_id=room, limit=10))
    # TODO: assert len(list(messages)) == 3
    pytest.fail("Implement this test")


# ---------------------------------------------------------------------------
# Task 3: Test error handling
# ---------------------------------------------------------------------------

def test_empty_content_is_rejected(stub):
    """Sending a message with empty content should raise INVALID_ARGUMENT."""
    # TODO: use pytest.raises(grpc.RpcError)
    # TODO: call stub.SendMessage with content=""
    # TODO: assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    pytest.fail("Implement this test")


# ---------------------------------------------------------------------------
# Bonus: Test SendBulkMessages (client streaming)
# ---------------------------------------------------------------------------

def test_send_bulk_messages(stub):
    """SendBulkMessages should report the correct count."""
    def _requests():
        for i in range(5):
            yield chat_pb2.MessageRequest(
                room_id="bulk-exercise", user="alice", content=f"bulk {i}"
            )
    # TODO: call stub.SendBulkMessages(_requests())
    # TODO: assert response.messages_sent == 5
    pytest.fail("Implement this test")
