# Exercise 2: First gRPC Service (30 min)

## Goal

Implement the **unary `SendMessage` RPC** — a server that stores messages in memory and a client that calls it.

## Prerequisites

```bash
# Make sure you have generated code:
poe generate
ls chat/generated/   # chat_pb2.py  chat_pb2_grpc.py
```

## Part A — Server (`server_starter.py`)

Open `server_starter.py`. You need to:

1. Create a `ChatServicer` class that inherits from `chat_pb2_grpc.ChatServiceServicer`
2. Implement `SendMessage(self, request, context)`:
   - Validate that `request.content` is not empty; if it is, call `context.abort(grpc.StatusCode.INVALID_ARGUMENT, "...")`
   - Generate a UUID for `message_id`
   - Save the message to an in-memory dict
   - Return `chat_pb2.MessageResponse(message_id=..., status="ok", timestamp=...)`
3. Implement `serve()` that starts the gRPC server on port 50051

## Part B — Client (`client_starter.py`)

Open `client_starter.py`. You need to:

1. Create an `insecure_channel` to `localhost:50051`
2. Create a `ChatServiceStub`
3. Call `stub.SendMessage(...)` with a `MessageRequest`
4. Print the returned `message_id` and `status`

## Run it

```bash
# Terminal 1 — start your server
python exercises/02_first_service/server_starter.py

# Terminal 2 — run the client
python exercises/02_first_service/client_starter.py

# Or use the CLI:
poe server   # (uses the reference implementation)
python -m chat.main client send --room general --user alice "Hello EuroPython!"
```

## Solution

`solutions/02_first_service/server.py` and `client.py`
