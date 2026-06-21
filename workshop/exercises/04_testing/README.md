# Exercise 4: Testing with pytest (20 min)

## Goal

Write integration tests that spin up a **real** gRPC server in-process — no mocks needed.

## Setup

The `conftest.py` already provides two fixtures:

| Fixture | Scope | What it gives you |
|---------|-------|-------------------|
| `grpc_addr` | session | Address of a running server, e.g. `"localhost:12345"` |
| `stub` | function | A fresh `ChatServiceStub` channel per test |

## Tasks

Open `test_starter.py` and implement the `TODO` items:

### Test 1 — `test_send_message_returns_id`

Call `stub.SendMessage(...)` and assert:
- `response.message_id` is not an empty string
- `response.status == "ok"`
- `response.timestamp > 0`

### Test 2 — `test_get_history_returns_messages`

1. Send 3 messages to room `"test-history"`
2. Call `stub.GetHistory(...)` with `limit=10`
3. Convert the stream to a list
4. Assert `len(messages) == 3`

### Test 3 — `test_empty_content_rejected`

Call `stub.SendMessage` with `content=""`, expect `grpc.RpcError` with code `INVALID_ARGUMENT`:

```python
import pytest, grpc

with pytest.raises(grpc.RpcError) as exc_info:
    stub.SendMessage(...)
assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
```

### Bonus — `test_send_bulk_messages`

Send 5 messages via `SendBulkMessages` and assert `messages_sent == 5`.

## Run

```bash
poe test
# or just this file:
pytest exercises/04_testing/test_starter.py -v
```

## Solution

`solutions/04_testing/test_chat.py`
