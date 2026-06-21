# Exercise 1: Protocol Buffers (30 min)

## Goal

Write the `.proto` schema for our Chat service from scratch.

## Background

Protocol Buffers is a language-neutral schema language. Every gRPC service starts with a `.proto` file that defines:
- **Messages** — the data structures (like dataclasses)
- **Services** — the RPC methods

Field numbers (= 1, 2, 3…) identify fields in the binary encoding.  
**Never change a field number after the schema is in use.**

## Your task

Open `chat_starter.proto` and fill in the `TODO` sections.

You need to define:

1. **`MessageRequest`** — sent by the client to post a message
   - `room_id` (string)
   - `user` (string)
   - `content` (string)

2. **`MessageResponse`** — returned after a successful send
   - `message_id` (string)
   - `status` (string) — `"ok"` or `"error"`
   - `timestamp` (int64) — Unix timestamp

3. **`HistoryRequest`** — request history for a room
   - `room_id` (string)
   - `limit` (int32) — max messages to return; 0 = all

4. **`BulkResponse`** — returned after a bulk upload
   - `messages_sent` (int32)
   - `messages_failed` (int32)

5. **`Message`** — a stored chat message
   - `message_id` (string)
   - `room_id` (string)
   - `user` (string)
   - `content` (string)
   - `timestamp` (int64)

6. **`ChatService`** with four RPCs:
   - `SendMessage(MessageRequest) → MessageResponse` — **unary**
   - `GetHistory(HistoryRequest) → stream Message` — **server streaming**
   - `SendBulkMessages(stream MessageRequest) → BulkResponse` — **client streaming**
   - `Chat(stream MessageRequest) → stream Message` — **bidirectional**

## Verify your proto

```bash
# From the workshop/ directory:
python -m grpc_tools.protoc \
  -I exercises/01_protocol_buffers \
  --python_out=/tmp/proto_check \
  --grpc_python_out=/tmp/proto_check \
  exercises/01_protocol_buffers/chat_starter.proto

echo "✓ No errors — proto is valid!"
```

Or use the project's real proto as your target:

```bash
poe generate
ls chat/generated/   # should show chat_pb2.py and chat_pb2_grpc.py
```

## Solution

`solutions/01_protocol_buffers/chat.proto`
