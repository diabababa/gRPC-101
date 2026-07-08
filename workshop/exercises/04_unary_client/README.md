# Exercise 4: Unary Client + Verify Communication (15 min)

## Goal

Write a client that calls `SendMessage` and see both sides talk to each other.

## Context

A gRPC client needs two objects:
- **Channel** — the connection to the server (one per process, reuse it)
- **Stub** — the auto-generated proxy that exposes RPC methods as Python functions

```
channel = grpc.insecure_channel("localhost:50051")
stub    = chat_pb2_grpc.ChatServiceStub(channel)
```

## Your task

Open `client_starter.py` and fill in the TODOs:

1. Create an `insecure_channel` to `"localhost:50051"` using a context manager:
   ```python
   with grpc.insecure_channel("localhost:50051") as channel:
   ```
2. Create a `ChatServiceStub` from the channel
3. Call `stub.SendMessage(...)` with a `MessageRequest`
   (fields: `room_id`, `user`, `content`)
4. Print `response.message_id` and `response.status`
5. Add a `try/except grpc.RpcError` to handle errors gracefully

## Run it

```bash
# Terminal 1 — start the server from Exercise 3
python exercises/03_unary_service/server_starter.py

# Terminal 2 — run your client
python exercises/04_unary_client/client_starter.py
# Expected output:
#   message_id: <uuid>
#   status:     ok
```

Try sending an empty message — what error code do you get?

## Solution

`solutions/04_unary_client/client.py`
