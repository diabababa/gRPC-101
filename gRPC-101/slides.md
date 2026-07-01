---
theme: seriph
background: https://cover.sli.dev
title: "gRPC for Beginners"
info: |
  ## gRPC for Beginners
  EuroPython 2026 — 3-hour hands-on workshop
  Build a real-time chat service with gRPC and Python
class: text-center
drawings:
  persist: false
transition: slide-left
duration: 180min
highlighter: shiki
lineNumbers: true
hideInToc: true
---

# gRPC for Beginners

Build a real-time chat service with Python

<div class="text-gray-400 mt-4">EuroPython 2026 · Kraków · 3h Workshop</div>

<div @click="$slidev.nav.next" class="mt-12 py-1" hover:bg="white op-10">
  Press Space to start <carbon:arrow-right />
</div>

<!--
Welcome everyone! Today you'll build a real chat service using gRPC — from proto definition to load testing. Laptop + Docker = you're ready.
-->

---
hideInToc: true
---

# About Us

<div class="grid grid-cols-2 gap-8 mt-8">
<div class="text-center">

**Kamil Kulig**

💼 Building at CTHINGS.CO  
🐍 Python lover · 🕺 King of Disco  
📢 PyCon Poland · PyCon Sweden · Python Warsaw

</div>
<div class="text-center">

**Adam Gorgoń**

📊 Data Scientist  
🧠 NLP & Statistics enthusiast  
🐍 Python & Machine Learning

</div>
</div>

---
hideInToc: true
---

# QR Code for repository

## TODO: add QR code
Workshop code: <strong>github.com/kamilkulig/grpc-101</strong>
## Project Setup

```bash
# Clone & enter workshop
cd workshop

# run test-exercises
docker compose run --rm workshop poe test-exercises

# Or create virtualenv and install deps and run
uv sync
source .venv/bin/activate
poe test-exercises
```

--- 
hideInToc: true
---

# Tech Stack 🛠️

<!-- # TODO: maybe delete to not shadow real goal: ruff, locust, prometeus grafana -->
> Disable your AI assistant — you'll learn more by writing the code yourself

<v-clicks>

- **PyCharm** has build in support for proto files, but VSCode needs plugin https://marketplace.visualstudio.com/items?itemName=bufbuild.vscode-buf
- **Docker** — infrastructure
- **uv** — fast package manager
- **poe** — task runner
- **pytest** — testing
- **ruff** — linter & formatter
- **locust** — load testing
- **Prometheus + Grafana** — monitoring

</v-clicks>

--- 
hideInToc: true
---

# What We'll Build Today
## Chat Service 💬

A real-time messaging service: 

* SendMessage, 
* GetHistory, 
* SendBulkMessages, 
* Chat

<!-- demonstrating **all 4 gRPC patterns**:

- `SendMessage` — unary call
- `GetHistory` — server streaming
- `SendBulkMessages` — client streaming
- `Chat` — bidirectional streaming
 -->

---
hideInToc: true
---


<Toc columns="3"/>

<!-- maybe add background agenda word -->
---
transition: fade-out
---

# What is RPC?

**Remote Procedure Call** — call a function on another machine as if it were local.

```
Client                          Server
  |                               |
  |  sayHello("Alice")  ───────►  |
  |                               |  execute sayHello()
  |  ◄───────── "Hello, Alice!"   |
  |                               |
```

<v-clicks>

- **Contract first** — define the interface before writing any code
- **Serialization is hidden** — framework converts objects to bytes and back
- **Transport is hidden** — you call a function; the network hop is invisible
- **Strongly typed** — both sides agree on types at compile time, not at runtime

</v-clicks>

---

# What is gRPC?

**gRPC** = Google Remote Procedure Call (open-sourced 2016, now [CNCF](https://en.wikipedia.org/wiki/Cloud_Native_Computing_Foundation))

<div class="grid grid-cols-2 gap-6 mt-6">
<div>

### Core components

```
┌─────────────────────┐
│   .proto file       │  ← You write this
│   (contract)        │
└────────┬────────────┘
         │ grpc_tools.protoc
    ┌────▼────┐   ┌────────┐
    │ Python  │   │  Go    │
    │  stubs  │   │ stubs  │
    └────┬────┘   └────────┘
         │
   HTTP/2 + Protobuf
```

</div>
<div>

### Why gRPC?

- **Binary format, no field names on the wire**
  
  <small class="text-gray-400">significantly smaller and faster than JSON</small>
- **4 communication patterns** — from simple request/response to full-duplex streaming
- **Strongly typed** contract
- **Auto-generated** clients in 10+ languages
- **Deadlines & cancellation** built in
  
  <small class="text-gray-400">Client sets a timeout; server auto-stops when deadline passes or client disconnects</small>

</div>
</div>

<!--
10x / 3x — these are typical figures from Google's own benchmarks and community benchmarks
(e.g. github.com/thekvs/cpp-serializers). The actual gain depends on message structure:
flat, numeric-heavy messages compress more than deeply nested string-heavy ones.
Tell participants: "treat these as order-of-magnitude, benchmark your own workload."

Deadlines & cancellation:
- REST: if the client disconnects, the server keeps running (no built-in signal).
- gRPC: the client can attach a deadline (e.g. 500 ms). If the server hasn't finished
  by then, the call is cancelled on both sides automatically. context.is_active()
  returns False so you can stop early and free resources.
  This matters a lot for streaming — you don't leak open streams when clients drop.
-->

---

# gRPC vs REST

<div class="overflow-auto max-h-100">

| Aspect | REST / HTTP | gRPC |
|---------|------------|------|
| Protocol | HTTP/1.1 | HTTP/2 |
| Format | JSON (text) | Protocol Buffers (binary) |
| Contract | OpenAPI (optional) | `.proto` (required) |
| Streaming | Limited (SSE, WebSocket) | 4 native patterns |
| Code gen | Optional | Built-in |
| Browser support | Native | Needs grpc-web proxy |
| Human readable | ✅ Yes | ❌ Binary |
| Performance | Good | Excellent |

</div>

---

# When to Use gRPC

<div class="grid grid-cols-2 gap-8 mt-4">
<div>

### ✅ Good fit

- Microservice-to-microservice communication
- Real-time bidirectional streaming (chat, IoT, gaming)
- Polyglot environments (Python + Go + Java)
- High-throughput, low-latency APIs
- Bandwidth-constrained clients — binary payloads use less data than JSON, matters on weak or metered connections (mobile data, IoT in the field, connected cars)

</div>
<div>

### ❌ Not the best fit

- Public APIs consumed by browsers directly
- Simple CRUD with occasional calls
- Teams unfamiliar with Protobuf
- Debugging / human inspection of traffic
- Simple scripts & one-off tools

</div>
</div>

<v-click>

> **Today's rule of thumb**: gRPC between services, REST at the edge

</v-click>

---
layout: two-cols
---

# Protocol Buffers — The Language of gRPC

**Protobuf** is a language-neutral schema language and binary serialization format.


  
```proto
syntax = "proto3";

package chat;

message MessageRequest {
  string room_id = 1;   // ← field number, NOT value
  string user    = 2;
  string content = 3;
}

message MessageResponse {
  string message_id = 1;
  string status = 2;
  int64 timestamp = 3;
}

service ChatService {
  rpc SendMessage (MessageRequest) returns (MessageResponse);
}
```

::right::

<!-- <div class="overflow-auto max-h-100"> -->

```proto
syntax = "proto3";

package example;

enum Status {
  UNKNOWN = 0; // proto3: first value MUST be 0
  ACTIVE = 1;
  BANNED = 2;
}

message Example {
  string name = 1;
  bytes data = 2;

  int32 count = 3;
  int64 size = 4;
  float score = 5;
  double precise = 6;

  bool active = 7;

  repeated string tags = 8;

  Status status = 9;
}


```


<!-- 
- Field numbers (1, 2, 3…) identify fields in binary — **never change them**
- Types: `string`, `int32`, `int64`, `bool`, `float`, `double`, `bytes`
- Collections: `repeated string tags = 4;`. Without `repeated`, a variable can have only one value
- Optional fields (proto3): all fields are optional by default 
-->
  

---

# Generate Message Classes

```bash
python -m grpc_tools.protoc \
  -I protos \                        # where to look for .proto imports `-I` can be repeated — useful when `.proto` files import from each other
  --python_out=chat/generated \      # message classes  → chat_pb2.py
  --pyi_out=chat/generated \         # type hints       → chat_pb2.pyi - `--pyi_out` generates `.pyi` stubs — autocomplete + mypy/pyright type checking
  protos/chat.proto

# Or just use the poe task we prepared:
poe generate-exercises
```
<v-clicks>


This produces **deterministic result**: (always produces identical output):

 `chat_pb2.py` — message classes (MessageRequest, MessageResponse…)

<!-- NOT SURE Keep generated files in a separate dir (`generated/`) and add to `.gitignore` -->

</v-clicks>


---

# 🛠️ Exercise 1: Proto Messages

Open `exercises/01_protocol_buffers/README.md`

<div class="grid grid-cols-2 gap-6 mt-4">
<div>



`MessageRequest` is filled in as an **example** — study the syntax, then define:

- `MessageResponse` — `message_id`, `status`, `timestamp`
- `Message` — `message_id`, `room_id`, `user`, `content`, `timestamp`
- `HistoryRequest` — `room_id`, `limit`
- `BulkResponse` — `messages_sent`, `messages_failed`

Field numbers start at 1.  
Types: `string`, `int32`, `int64`

</div>
<div>

### Verify

```bash
poe generate-exercises
# No errors → code generated in exercises/generated/
```

Peek at `exercises/generated/chat_pb2.py` —  
each proto message becomes a Python class!

Solution: `solutions/01_protocol_buffers/chat.proto`

</div>
</div>

---

# Defining a gRPC Service

```proto
syntax = "proto3";

package chat;

service ChatService {
  // Unary: one request → one response
  rpc SendMessage (MessageRequest) returns (MessageResponse);

  // Server streaming: one request → stream of responses
  rpc GetHistory (HistoryRequest) returns (stream Message);

  // Client streaming: stream of requests → one response
  rpc SendBulkMessages (stream MessageRequest) returns (BulkResponse);

  // Bidirectional: stream of requests → stream of responses
  rpc Chat (stream MessageRequest) returns (stream Message);
}
```

<v-click>

`stream` keyword = the only difference between the 4 patterns!

</v-click>

---

# Generate Service Stubs

```bash
python -m grpc_tools.protoc \
  -I protos \                        # where to look for .proto imports `-I` can be repeated — useful when `.proto` files import from each other
  --python_out=chat/generated \      # message classes  → chat_pb2.py
  --grpc_python_out=chat/generated \ # service stubs    → chat_pb2_grpc.py
  --pyi_out=chat/generated \         # type hints       → chat_pb2.pyi - `--pyi_out` generates `.pyi` stubs — autocomplete + mypy/pyright type checking
  protos/chat.proto

# Or just use the poe task we prepared:
poe generate
```
<v-clicks>


This produces **deterministic result**: (always produces identical output):

- `chat_pb2.py` — message classes (MessageRequest, MessageResponse…)
- `chat_pb2_grpc.py` — service stubs (ChatServiceStub, ChatServiceServicer…)

</v-clicks>


---

# 🛠️ Exercise 2: Build a Service Stub

Open `exercises/02_service_stub/README.md`

<div class="grid grid-cols-2 gap-6 mt-4">
<div>



Open `server_starter.py` and:

1. Create `ChatServicer` inheriting from `chat_pb2_grpc.ChatServiceServicer`
2. Add the four RPC methods — all return `pass` for now:
   - `SendMessage(self, request, context)`
   - `GetHistory(self, request, context)`
   - `SendBulkMessages(self, request_iterator, context)`
   - `Chat(self, request_iterator, context)`
3. Register with the server and start it

</div>
<div>

### Verify

```bash
python exercises/02_service_stub/server_starter.py
# Server listening on :50051
```

The server starts — every call returns an error (no logic yet).  
That's expected. Logic comes in Exercise 3.

Solution: `solutions/02_service_stub/server.py`

</div>
</div>

---

# The Server — Implementing ChatServicer

<div class="overflow-auto max-h-100">

```python {all|1-3|6-10|12-20|22-27}
import grpc
from concurrent import futures
from chat.generated import chat_pb2, chat_pb2_grpc

# Your servicer inherits from the generated base class
class ChatServicer(chat_pb2_grpc.ChatServiceServicer):

    def __init__(self):
        self._store: dict[str, list] = {}  # room_id → [Message]

    def SendMessage(self, request, context):
        # request: MessageRequest
        # context: grpc.ServicerContext (deadlines, metadata, cancel)
        msg = self._save_message(request)
        return chat_pb2.MessageResponse(
            message_id=msg.message_id,
            status="ok",
            timestamp=msg.timestamp,
        )

def serve(port: int = 50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()
```

</div>

---

# 🛠️ Exercise 3: Implement Unary SendMessage

Open `exercises/03_unary_service/README.md`

<div class="grid grid-cols-2 gap-6 mt-4">
<div>



Open `exercises/03_unary_service/server_starter.py` and fill in `SendMessage`:

1. **Validate** — abort with `INVALID_ARGUMENT` if `request.content` is empty
2. **Save** — call `_make_message(request)` to persist and get a `Message`
3. **Return** — a `MessageResponse(message_id=..., status="ok", timestamp=...)`

</div>
<div>

### Test it

```bash
# Terminal 1
python exercises/03_unary_service/server_starter.py

# Terminal 2
poe client-send --room general --user alice "Hello!"
# ✓ Sent  id=<uuid>  status=ok
```

Solution: `solutions/03_unary_service/server.py`

</div>
</div>



---

# The Client — Stubs and Channels

```python {all|1-6|8-14|16-22}
import grpc
from chat.generated import chat_pb2, chat_pb2_grpc

# Channel = connection to server (reuse across calls)
channel = grpc.insecure_channel("localhost:50051")
stub = chat_pb2_grpc.ChatServiceStub(channel)

# Unary call — just like a local function
response = stub.SendMessage(
    chat_pb2.MessageRequest(
        room_id="general",
        user="alice",
        content="Hello, EuroPython!",
    )
)
print(f"Message ID: {response.message_id}")

# With context manager (auto-closes channel)
with grpc.insecure_channel("localhost:50051") as channel:
    stub = chat_pb2_grpc.ChatServiceStub(channel)
    response = stub.SendMessage(...)
```


---

# 🛠️ Exercise 4: Unary Client + Verify Communication



Open `exercises/04_unary_client/README.md`

<div class="grid grid-cols-2 gap-6 mt-4">
<div>


Open `exercises/04_unary_client/client_starter.py` and:

1. Open an `insecure_channel` to `"localhost:50051"`
2. Create a `ChatServiceStub` from the channel
3. Call `stub.SendMessage(...)` with a `MessageRequest`
4. Print `response.message_id` and `response.status`
5. Catch `grpc.RpcError` and print `e.code()` + `e.details()`


</div>
<div>

### Verify both sides talk

```bash
# Terminal 1 — server from Exercise 3
python exercises/03_unary_service/server_starter.py

# Terminal 2 — your client
python exercises/04_unary_client/client_starter.py
# message_id: <uuid>
# status:     ok
```

Try an empty message — what error code appears?

Solution: `solutions/04_unary_client/client.py`

</div>
</div>

---

# Communication Patterns

<div class="grid grid-cols-2 gap-4 mt-4">

<div>

### 1. Unary (request-response)
```python
response = stub.SendMessage(request)
```
Use for: simple lookups, mutations

### 2. Server streaming
```python
for msg in stub.GetHistory(request):
    print(msg.content)
```
Use for: feeds, file downloads, live updates

</div>
<div>

### 3. Client streaming
```python
def requests():
    for msg in messages:
        yield msg

response = stub.SendBulkMessages(requests())
```
Use for: file uploads, bulk inserts

### 4. Bidirectional streaming
```python
def requests():
    for msg in user_input():
        yield msg

for reply in stub.Chat(requests()):
    print(reply.content)
```
Use for: chat, gaming, real-time collaboration

</div>
</div>

---

# Server Streaming — Implementation

```python
# Server side — yield messages one by one
def GetHistory(self, request, context):
    messages = self._store.get(request.room_id, [])
    limit = request.limit or len(messages)
    for msg in messages[-limit:]:
        yield msg  # ← just yield, gRPC handles the stream

# Client side — iterate like any Python generator
for message in stub.GetHistory(
    chat_pb2.HistoryRequest(room_id="general", limit=10)
):
    print(f"[{message.user}]: {message.content}")
```

---

# Bidirectional Streaming — Implementation

```python
# Server side — iterate request stream, yield responses
def Chat(self, request_iterator, context):
    for request in request_iterator:
        msg = self._save_message(request)
        yield msg  # echo back as Message

# Client side — generator feeds requests, iterate responses
import threading

def user_messages():
    for line in sys.stdin:
        yield chat_pb2.MessageRequest(
            room_id="general",
            user="alice",
            content=line.strip(),
        )

for reply in stub.Chat(user_messages()):
    print(f"[{reply.user}]: {reply.content}")
```

---

# 🛠️ Exercise 5: Streaming Patterns

Open `exercises/05_streaming/README.md`

<div class="grid grid-cols-2 gap-6 mt-4">
<div>

### Tasks

1. Implement `GetHistory` (server streaming) in the servicer
2. Implement the client loop that prints streamed messages
3. *Bonus:* implement `SendBulkMessages` (client streaming)
4. *Bonus:* implement `Chat` (bidirectional)

</div>
<div>

### Test it

```bash
# Start server
poe server

# Get history (server streaming)
python -m exercises.main client history \
  --room general --limit 5

# Bidirectional chat
python -m exercises.main client chat \
  --room general --user alice
```

</div>
</div>

---

# Error Handling in gRPC

```python
import grpc

# Server — set status codes
def SendMessage(self, request, context):
    if not request.content:
        context.abort(
            grpc.StatusCode.INVALID_ARGUMENT,
            "Message content cannot be empty",
        )
    ...

# Client — catch RpcError
try:
    response = stub.SendMessage(request)
except grpc.RpcError as e:
    print(f"Code: {e.code()}")       # grpc.StatusCode.INVALID_ARGUMENT
    print(f"Details: {e.details()}")  # "Message content cannot be empty"
```

Common status codes: `OK`, `NOT_FOUND`, `INVALID_ARGUMENT`, `UNAUTHENTICATED`, `PERMISSION_DENIED`, `DEADLINE_EXCEEDED`, `UNAVAILABLE`


---

# Key Takeaways

<v-clicks>

1. **gRPC = Protobuf + HTTP/2 + Code gen** — fast, typed, polyglot

2. **4 patterns** — unary, server streaming, client streaming, bidirectional

3. **Proto contract is the source of truth** — define it carefully, field numbers are forever

4. **Testing is straightforward** — start a real server in your fixture, test against it

5. **Locust + Prometheus/Grafana** — measure before optimizing

6. **gRPC shines in microservices** — use REST at the edge, gRPC between services

</v-clicks>

---
hideInToc: true
---

# What's Next?

<div class="grid grid-cols-2 gap-6 mt-4">
<div>

### Go deeper

- **TLS / mTLS** — secure your gRPC channels
- **Interceptors** — middleware for auth, logging, tracing
- **gRPC-Web** — use gRPC from browsers
- **OpenTelemetry** — distributed tracing
- **Server reflection** — dynamic service discovery (grpcurl)

</div>
<div>

### Resources

- `grpc.io/docs` — official docs
- `github.com/grpc/grpc` — gRPC repo
- `buf.build` — modern proto toolchain
- `github.com/fullstorydev/grpcurl` — curl for gRPC
- Workshop repo: `github.com/kamilkulig/grpc-101`

</div>
</div>

---
layout: center
class: text-center
hideInToc: true
---

# Q & A

<div class="text-6xl mt-8">🙋</div>

<div class="mt-8 text-gray-400">
Workshop code: <strong>github.com/kamilkulig/grpc-101</strong>
</div>

TODO: ADD QR code to linkedin
<div class="mt-4 text-gray-400">
Kamil Kulig · Adam Gorgoń
</div>

<!--
Thank you! Any questions? Feel free to keep working on exercises — we'll be around for the rest of the workshop.
-->
