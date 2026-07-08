# Exercise 2: Build a Service Stub (10 min)

## Goal

Create the `ChatServicer` class — the Python object that will handle incoming
gRPC calls. In this exercise you only need the **structure** (no logic yet).

## Context

After running `poe generate-exercises`, grpc_tools produced
`exercises/generated/chat_pb2_grpc.py`. Open it and find
`ChatServiceServicer` — this is the base class you must inherit from.

## Your task

Open `server_starter.py` and:

1. Create `ChatServicer` that inherits from `chat_pb2_grpc.ChatServiceServicer`
2. Add these four methods (all return `pass` for now):
   - `SendMessage(self, request, context)`
   - `GetHistory(self, request, context)`
   - `SendBulkMessages(self, request_iterator, context)`
   - `Chat(self, request_iterator, context)`
3. In `serve()`, register your servicer with the server using
   `chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)`

## Run it

```bash
python exercises/02_first_service/server_starter.py
# Should print: Server listening on :50051
# Ctrl-C to stop
```

The server starts but returns gRPC errors on every call — that's expected.
We'll add the real logic in Exercise 3.

## Solution

`solutions/02_service_stub/server.py`
