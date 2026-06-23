"""
Complete implementation of ChatServicer — solution for all exercises.
Used by poe test-solutions so tests always pass regardless of participant progress.
"""
import time
import uuid

import grpc

from chat.generated import chat_pb2, chat_pb2_grpc

_store: dict[str, list[chat_pb2.Message]] = {}


def _make_message(request: chat_pb2.MessageRequest) -> chat_pb2.Message:
    msg = chat_pb2.Message(
        message_id=str(uuid.uuid4()),
        room_id=request.room_id,
        user=request.user,
        content=request.content,
        timestamp=int(time.time()),
    )
    _store.setdefault(request.room_id, []).append(msg)
    return msg


class SolutionChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def SendMessage(self, request, context):
        if not request.content.strip():
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Message content cannot be empty")
        msg = _make_message(request)
        return chat_pb2.MessageResponse(
            message_id=msg.message_id, status="ok", timestamp=msg.timestamp
        )

    def GetHistory(self, request, context):
        messages = _store.get(request.room_id, [])
        limit = request.limit if request.limit > 0 else len(messages)
        for msg in messages[-limit:]:
            yield msg

    def SendBulkMessages(self, request_iterator, context):
        sent = failed = 0
        for request in request_iterator:
            try:
                _make_message(request)
                sent += 1
            except Exception:
                failed += 1
        return chat_pb2.BulkResponse(messages_sent=sent, messages_failed=failed)

    def Chat(self, request_iterator, context):
        for request in request_iterator:
            if context.is_active():
                yield _make_message(request)
