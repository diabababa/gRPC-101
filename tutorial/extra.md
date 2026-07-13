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

# 🛠️ Exercise 6: Testing 

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

# 🛠️ Exercise 7: Performance 

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

# 🛠️ Exercise 8: Monitoring 

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
