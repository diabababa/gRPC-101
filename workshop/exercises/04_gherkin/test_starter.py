"""Exercise 4 — write pytest tests for the gRPC Chat service.

Run with:
    pytest exercises/04_gherkin/test_starter.py -v
"""

import pytest
import grpc

from chat.generated import chat_pb2

# conftest.py in exercises/ provides the `stub` fixture automatically.


# ---------------------------------------------------------------------------
# Task 1: Test SendMessage (unary)
# ---------------------------------------------------------------------------

def test_send_message_returns_id(stub):
    """Calling SendMessage should return a non-empty message_id and status 'ok'."""
    response = stub.SendMessage(
        chat_pb2.MessageRequest(
            # TODO: fill in room_id, user, content
        )
    )
    # TODO: assert response.message_id != ""
    # TODO: assert response.status == "ok"
    # TODO: assert response.timestamp > 0


# ---------------------------------------------------------------------------
# Task 2: Test GetHistory (server streaming)
# ---------------------------------------------------------------------------

def test_get_history_returns_messages(stub):
    """After sending 3 messages, GetHistory should stream all 3 back."""
    room = "exercise-history"

    # TODO: send 3 messages to room using stub.SendMessage in a loop

    # TODO: call stub.GetHistory with HistoryRequest(room_id=room, limit=10)
    # TODO: convert to list: messages = list(...)

    # TODO: assert len(messages) == 3


# ---------------------------------------------------------------------------
# Task 3: Test error handling
# ---------------------------------------------------------------------------

def test_empty_content_is_rejected(stub):
    """Sending a message with empty content should raise INVALID_ARGUMENT."""
    # TODO: use pytest.raises(grpc.RpcError) context manager
    # TODO: call stub.SendMessage with content=""
    # TODO: assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    pass


# ---------------------------------------------------------------------------
# Bonus: Test SendBulkMessages (client streaming)
# ---------------------------------------------------------------------------

def test_send_bulk_messages(stub):
    """SendBulkMessages should report the correct count."""
    def _requests():
        for i in range(5):
            yield chat_pb2.MessageRequest(
                room_id="bulk-exercise",
                user="alice",
                content=f"bulk {i}",
            )

    # TODO: call stub.SendBulkMessages(_requests())
    # TODO: assert response.messages_sent == 5
    pass
