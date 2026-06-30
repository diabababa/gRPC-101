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


--- 
hideInToc: true
---

# What We'll Build Today

<div class="grid grid-cols-2 gap-8 mt-6">
<div>

## Chat Service 💬

A real-time messaging service demonstrating **all 4 gRPC patterns**:

- `SendMessage` — unary call
- `GetHistory` — server streaming
- `SendBulkMessages` — client streaming
- `Chat` — bidirectional streaming

> Disable your AI assistant — you'll learn more by writing the code yourself

</div>
<div>

## Tech Stack 🛠️

- **uv** — fast package manager
- **poe** — task runner
- **ruff** — linter & formatter
- **pytest** — testing
- **locust** — load testing
- **Prometheus + Grafana** — monitoring
- **Docker** — infrastructure

</div>
</div>

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
```

<v-clicks>

- Field numbers (1, 2, 3…) identify fields in binary — **never change them**
- Types: `string`, `int32`, `int64`, `bool`, `float`, `double`, `bytes`
- Collections: `repeated string tags = 4;`. Without `repeated`, a variable can have only one value
- Optional fields (proto3): all fields are optional by default

</v-clicks>

---

# Proto Data Types Cheat Sheet
<div class="overflow-auto max-h-100">
```proto
message Example {
  // Strings & bytes
  string name     = 1;
  bytes  data     = 2;

  // Numbers
  int32  count    = 3;
  int64  size     = 4;
  float  score    = 5;
  double precise  = 6;

  // Boolean
  bool   active   = 7;

  // Repeated (list)
  repeated string tags = 8;

  // Enum
  Status status = 9;
}

enum Status {
  UNKNOWN = 0;   // proto3: first value MUST be 0
  ACTIVE  = 1;
  BANNED  = 2;
}
```
</div>


---

# Code Generation

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



This produces:

- `chat_pb2.py` — message classes (MessageRequest, MessageResponse…)
- `chat_pb2_grpc.py` — service stubs (ChatServiceStub, ChatServiceServicer…)

**Deterministic** — same `.proto` always produces identical output; CI can verify nobody edited generated files by hand
 
Keep generated files in a separate dir (`generated/`) and add to `.gitignore`

</v-clicks>


---

# Project Setup

```bash
# Clone & enter workshop
cd workshop

# Create virtualenv and install deps
uv sync

# Generate gRPC code from .proto
poe generate

# Verify
ls chat/generated/
# chat_pb2.py  chat_pb2_grpc.py
```

<v-click>

### Available poe tasks

```bash
poe generate   # generate stubs from protos/chat.proto
poe server     # start gRPC server (port 50051)
poe test       # run pytest
poe lint       # ruff check
poe fmt        # ruff format
poe locust     # start Locust UI
```

</v-click>

---

# 🛠️ Exercise 1: Proto Messages (15 min)

Open `exercises/01_protocol_buffers/README.md`

<div class="grid grid-cols-2 gap-6 mt-4">
<div>

### Your task

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

# 🛠️ Exercise 2: Build a Service Stub (10 min)

Open `exercises/02_service_stub/README.md`

<div class="grid grid-cols-2 gap-6 mt-4">
<div>

### Your task

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

# 🛠️ Exercise 3: Implement Unary SendMessage (15 min)

Open `exercises/03_unary_service/README.md`

<div class="grid grid-cols-2 gap-6 mt-4">
<div>

### Your task

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

# 🛠️ Exercise 4: Unary Client + Verify Communication (15 min)

Open `exercises/04_unary_client/README.md`

<div class="grid grid-cols-2 gap-6 mt-4">
<div>

### Your task

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

# 🛠️ Exercise 5: Streaming Patterns (20 min)

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

# Testing gRPC Services with pytest

```python
# tests/conftest.py
import pytest
import grpc
from concurrent import futures
from chat.server import ChatServicer
from chat.generated import chat_pb2_grpc

@pytest.fixture(scope="session")
def grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    port = server.add_insecure_port("[::]:0")  # OS picks a free port
    server.start()
    yield f"localhost:{port}"
    server.stop(grace=None)

@pytest.fixture
def stub(grpc_server):
    with grpc.insecure_channel(grpc_server) as channel:
        yield chat_pb2_grpc.ChatServiceStub(channel)
```

---

# Writing gRPC Tests


<div class="overflow-auto max-h-100">

```python
# tests/test_chat.py
from chat.generated import chat_pb2

def test_send_message_returns_message_id(stub):
    response = stub.SendMessage(
        chat_pb2.MessageRequest(
            room_id="test-room",
            user="alice",
            content="Hello!",
        )
    )
    assert response.message_id != ""
    assert response.status == "ok"

def test_get_history_streams_messages(stub):
    # Send 3 messages first
    for i in range(3):
        stub.SendMessage(chat_pb2.MessageRequest(
            room_id="history-room", user="alice", content=f"msg {i}"
        ))

    messages = list(stub.GetHistory(
        chat_pb2.HistoryRequest(room_id="history-room", limit=10)
    ))
    assert len(messages) == 3
```

</div>

---

# 🛠️ Exercise 6: Testing (20 min)

Open `exercises/06_testing/README.md`

<div class="grid grid-cols-2 gap-6 mt-4">
<div>

### Tasks

1. Write a test for `SendMessage` — verify message_id and status
2. Write a test for `GetHistory` — verify correct count of messages
3. Write a test for error handling — send empty content, expect `INVALID_ARGUMENT`
4. *Bonus:* test `SendBulkMessages`

</div>
<div>

### Run tests

```bash
poe test-exercises

# or verbose
pytest tests/exercises/ -v

# run specific test
pytest tests/exercises/ -k test_send_message -v
```

</div>
</div>

---

# Performance Testing with Locust

**Locust** — load testing in pure Python. Simulates concurrent users sending requests.

```python
# tests/locustfile.py
from locust import User, task, between, events
import grpc, time
from chat.generated import chat_pb2, chat_pb2_grpc

class GrpcUser(User):
    abstract = True

    def on_start(self):
        self._channel = grpc.insecure_channel("localhost:50051")
        self._stub = chat_pb2_grpc.ChatServiceStub(self._channel)

class ChatUser(GrpcUser):
    wait_time = between(0.5, 2)  # random wait between tasks

    @task(3)  # weight: called 3x more than other tasks
    def send_message(self):
        self._stub.SendMessage(chat_pb2.MessageRequest(
            room_id="perf-room",
            user="locust",
            content="Load test message",
        ))
```

---

# Running Locust

```bash
# Start server
poe server-solutions

# Start Locust UI (web interface)
poe locust
# Open http://localhost:8089

# Or headless (CLI mode)
locust -f solutions/07_performance/locustfile.py \
  --headless \
  --users 50 \
  --spawn-rate 5 \
  --run-time 30s
```

<v-click>

### Key metrics to watch

- **RPS** (requests per second) — throughput
- **p50 / p95 / p99** — latency percentiles
- **Failures %** — error rate

</v-click>

---

# 🛠️ Exercise 7: Performance (20 min)

Open `exercises/07_performance/README.md`

<div class="grid grid-cols-2 gap-6 mt-4">
<div>

### Tasks

1. Complete `locustfile_starter.py` — add `send_message` task
2. Add `get_history` task (weight 1)
3. Start server + locust:
   ```bash
   poe server &
   poe locust
   ```
4. Ramp to 100 users, observe metrics
5. *Bonus:* add `SendBulkMessages` task

</div>
<div>

### Questions to answer

- What's the max RPS before failures appear?
- What's the p99 latency at 50 users?
- Which endpoint is slowest? Why?

</div>
</div>

---

# Monitoring gRPC with Prometheus

```python
# chat/server.py
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter(
    "grpc_requests_total",
    "Total gRPC requests",
    ["method", "status"],
)
REQUEST_LATENCY = Histogram(
    "grpc_request_duration_seconds",
    "gRPC request duration",
    ["method"],
)

class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def SendMessage(self, request, context):
        with REQUEST_LATENCY.labels(method="SendMessage").time():
            result = self._handle(request, context)
            REQUEST_COUNT.labels(method="SendMessage", status="ok").inc()
            return result

# Expose metrics on port 8000
start_http_server(8000)
```

---

# Prometheus + Grafana with Docker Compose

```bash
# Start the full monitoring stack
docker compose up -d

# Services:
# - chat-server  → localhost:50051  (gRPC)
# - prometheus   → localhost:9090   (metrics scraping)
# - grafana      → localhost:3000   (dashboards)
#   login: admin / admin
```

<v-click>

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: grpc-chat
    static_configs:
      - targets: ["chat-server:8000"]
```

</v-click>

---

# 🛠️ Exercise 8: Monitoring (20 min)

```bash
# Start everything
docker compose up -d

# Send some traffic
for i in $(seq 1 50); do
  python -m chat.main client send \
    --room general --user alice "Message $i"
done

# Or use locust to generate load
poe locust --headless --users 20 --spawn-time 5 --run-time 30s
```

<v-click>

### In Grafana (localhost:3000)

1. Login: `admin` / `admin`
2. Open Dashboard → **gRPC Chat Service**
3. Observe: request rate, latency, error rate
4. Try breaking the server — what happens to metrics?

</v-click>

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

<div class="mt-4 text-gray-400">
Kamil Kulig · Adam Gorgoń
</div>

<!--
Thank you! Any questions? Feel free to keep working on exercises — we'll be around for the rest of the workshop.
-->
