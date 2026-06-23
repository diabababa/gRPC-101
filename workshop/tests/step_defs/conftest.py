"""
Shared step definitions for all Gherkin feature files.
Fixtures (grpc_addr, stub) are inherited from tests/conftest.py.
"""
import time
from concurrent.futures import ThreadPoolExecutor

import grpc
import pytest
from pytest_bdd import given, parsers, then, when

from chat.generated import chat_pb2, chat_pb2_grpc


# ---------------------------------------------------------------------------
# Proto / schema steps (Exercise 01)
# ---------------------------------------------------------------------------

@given("the proto schema is compiled", target_fixture="proto_modules")
def proto_modules_fixture():
    return {"pb2": chat_pb2, "grpc": chat_pb2_grpc}


@when("I inspect the generated module")
def _inspect_module(proto_modules):
    pass


@when("I inspect the ChatServiceStub")
def _inspect_stub(proto_modules):
    pass


@then("MessageRequest can be created with room_id, user, and content")
def _check_message_request(proto_modules):
    msg = proto_modules["pb2"].MessageRequest(room_id="r", user="u", content="c")
    assert msg.room_id == "r"
    assert msg.user == "u"
    assert msg.content == "c"


@then("MessageResponse has message_id, status, and timestamp fields")
def _check_message_response(proto_modules):
    resp = proto_modules["pb2"].MessageResponse(message_id="id", status="ok", timestamp=1)
    assert resp.message_id == "id"
    assert resp.status == "ok"
    assert resp.timestamp == 1


@then("HistoryRequest has room_id and limit fields")
def _check_history_request(proto_modules):
    req = proto_modules["pb2"].HistoryRequest(room_id="room", limit=5)
    assert req.room_id == "room"
    assert req.limit == 5


@then("Message has all five fields")
def _check_message(proto_modules):
    msg = proto_modules["pb2"].Message(
        message_id="id", room_id="r", user="u", content="c", timestamp=1
    )
    assert msg.message_id == "id"
    assert msg.room_id == "r"
    assert msg.user == "u"
    assert msg.content == "c"
    assert msg.timestamp == 1


@then(parsers.parse('it has a "{method}" method'))
def _check_stub_method(stub, method):
    assert hasattr(stub, method), f"ChatServiceStub has no method '{method}'"


# ---------------------------------------------------------------------------
# Service / unary steps (Exercises 02, 04)
# ---------------------------------------------------------------------------

@given("the Chat service is running")
def _service_running(stub):
    assert stub is not None


@when(
    parsers.parse(
        'I send a message to room "{room}" as user "{user}" with content "{content}"'
    ),
    target_fixture="send_response",
)
def _send_message(stub, room, user, content):
    return stub.SendMessage(
        chat_pb2.MessageRequest(room_id=room, user=user, content=content)
    )


@when("I send two messages to room \"unique-test\"", target_fixture="two_responses")
def _send_two_messages(stub):
    r1 = stub.SendMessage(
        chat_pb2.MessageRequest(room_id="unique-test", user="alice", content="first")
    )
    r2 = stub.SendMessage(
        chat_pb2.MessageRequest(room_id="unique-test", user="alice", content="second")
    )
    return r1, r2


@when("I send a message with empty content", target_fixture="grpc_error")
def _send_empty_content(stub):
    try:
        stub.SendMessage(
            chat_pb2.MessageRequest(room_id="room", user="alice", content="")
        )
        return None
    except grpc.RpcError as e:
        return e


@then("I receive a response with a non-empty message_id")
def _check_message_id(send_response):
    assert send_response.message_id != ""


@then(parsers.parse('the response status is "{status}"'))
def _check_status(send_response, status):
    assert send_response.status == status


@then("the response has a positive timestamp")
def _check_timestamp(send_response):
    assert send_response.timestamp > 0


@then("each message has a different message_id")
def _check_unique_ids(two_responses):
    r1, r2 = two_responses
    assert r1.message_id != r2.message_id


@then("the service returns status code INVALID_ARGUMENT")
def _check_invalid_argument(grpc_error):
    assert grpc_error is not None
    assert grpc_error.code() == grpc.StatusCode.INVALID_ARGUMENT


# ---------------------------------------------------------------------------
# Streaming steps (Exercise 03, 04)
# ---------------------------------------------------------------------------

@given(parsers.parse("{n:d} messages were sent to room \"{room}\""))
def _seed_messages(stub, n, room):
    for i in range(n):
        stub.SendMessage(
            chat_pb2.MessageRequest(room_id=room, user="seed", content=f"seed msg {i}")
        )


@when(
    parsers.parse('I request history for room "{room}" with limit {limit:d}'),
    target_fixture="history_messages",
)
def _get_history(stub, room, limit):
    return list(stub.GetHistory(chat_pb2.HistoryRequest(room_id=room, limit=limit)))


@when(
    parsers.parse("I stream {n:d} messages to room \"{room}\""),
    target_fixture="bulk_response",
)
def _send_bulk(stub, n, room):
    def _requests():
        for i in range(n):
            yield chat_pb2.MessageRequest(room_id=room, user="bulk", content=f"bulk {i}")

    return stub.SendBulkMessages(_requests())


@when(
    parsers.parse(
        "I send {n:d} messages through the bidirectional Chat stream to room \"{room}\""
    ),
    target_fixture="chat_replies",
)
def _bidi_chat(stub, n, room):
    def _requests():
        for i in range(n):
            yield chat_pb2.MessageRequest(room_id=room, user="alice", content=f"bidi {i}")

    return list(stub.Chat(_requests()))


@then(parsers.parse("I receive a stream of {n:d} messages"))
def _check_stream_length(history_messages, n):
    assert len(history_messages) == n


@then(parsers.parse("the service reports {n:d} messages sent"))
def _check_bulk_count(bulk_response, n):
    assert bulk_response.messages_sent == n


@then(parsers.parse("I receive {n:d} echoed messages back"))
def _check_bidi_replies(chat_replies, n):
    assert len(chat_replies) == n


# ---------------------------------------------------------------------------
# Performance steps (Exercise 05)
# ---------------------------------------------------------------------------

@when(
    parsers.parse(
        "I send {n:d} messages concurrently with {workers:d} worker threads to room \"{room}\""
    ),
    target_fixture="perf_results",
)
def _send_concurrent(grpc_addr, n, workers, room):
    times = []
    errors = []

    def _send_one(i):
        t0 = time.perf_counter()
        try:
            with grpc.insecure_channel(grpc_addr) as ch:
                s = chat_pb2_grpc.ChatServiceStub(ch)
                s.SendMessage(
                    chat_pb2.MessageRequest(room_id=room, user="perf", content=f"msg {i}")
                )
            return time.perf_counter() - t0
        except grpc.RpcError as e:
            errors.append(e)
            return None

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(_send_one, range(n)))

    times = [t for t in results if t is not None]
    return {"times": times, "errors": errors, "total": n}


@when(
    parsers.parse('I send {n:d} messages sequentially to room "{room}"'),
    target_fixture="perf_results",
)
def _send_sequential(stub, n, room):
    times = []
    errors = []

    for i in range(n):
        t0 = time.perf_counter()
        try:
            stub.SendMessage(
                chat_pb2.MessageRequest(room_id=room, user="perf", content=f"seq {i}")
            )
            times.append(time.perf_counter() - t0)
        except grpc.RpcError as e:
            errors.append(e)

    return {"times": times, "errors": errors, "total": n}


@then("all requests succeed")
def _check_all_succeed(perf_results):
    assert len(perf_results["errors"]) == 0
    assert len(perf_results["times"]) == perf_results["total"]


@then(parsers.parse("the average response time is under {ms:d}ms"))
def _check_avg_latency(perf_results, ms):
    avg_ms = (sum(perf_results["times"]) / len(perf_results["times"])) * 1000
    assert avg_ms < ms, f"Average latency {avg_ms:.1f}ms exceeded limit {ms}ms"
