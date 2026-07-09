# Exercise 3: Implement Unary SendMessage (15 min)

## Goal

Add real logic to `SendMessage` so the server actually stores and acknowledges
messages.

## Context

A **unary RPC** works like a normal function call: one request in, one response
out. The servicer method receives:
- `request` — the `MessageRequest` proto object (fields: `room_id`, `user`, `content`)
- `context` — lets you set error codes, deadlines, metadata

## Your task

Open `exercises/server.py` and implement `SendMessage` inside the
`ChatServicer` class:

1. **Validate** — if `request.content` is empty, abort:
   ```python
   context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Message content cannot be empty")
   ```
2. **Save** — call `_make_message(request)` which stores the message and
   returns a `Message` proto with `message_id` and `timestamp` already set
3. **Return** — a `MessageResponse`:
   ```python
   return chat_pb2.MessageResponse(
       message_id=msg.message_id,
       status="ok",
       timestamp=msg.timestamp,
   )
   ```

## Run it

```bash
# Terminal 1
poe server
# gRPC server listening on :50051
# Prometheus metrics at http://localhost:8000/metrics

# Terminal 2 — quick smoke test with the CLI
poe client-send --room general --user alice "Hello!"
# ✓ Sent  id=<uuid>  status=ok
```

## Solution

`solutions/03_unary_service/server.py`
