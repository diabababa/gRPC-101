# gRPC for Beginners — Workshop

**EuroPython 2026 · Kraków · 3h hands-on workshop**

Build a real-time **Chat Service** using gRPC and Python, covering all four communication patterns, testing, load testing, and monitoring.

---

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Docker + Docker Compose

---

## Quick start

```bash
# 1. Install dependencies
uv sync

# 2. Generate gRPC code from .proto
poe generate

# 3. Start the server
poe server

# 4. In another terminal — send a message
python -m exercises.main client send --room general --user alice "Hello EuroPython!"

# 5. Get history
python -m exercises.main client history --room general

# 6. Interactive chat (bidirectional streaming)
python -m exercises.main client chat --room general --user alice
```

---

## Available poe tasks

| Task | Description |
|------|-------------|
| `poe generate` | Generate Python stubs from `protos/chat.proto` |
| `poe server` | Start gRPC server on port 50051 |
| `poe test` | Run pytest test suite |
| `poe lint` | Ruff linter |
| `poe fmt` | Ruff formatter |
| `poe locust` | Start Locust UI at http://localhost:8089 |

---

## Workshop agenda

| # | Topic | Time | Files |
|---|-------|------|-------|
| 1 | Protocol Buffers | 30 min | `exercises/01_protocol_buffers/` |
| 2 | First gRPC Service | 30 min | `exercises/02_first_service/` |
| 3 | Streaming Patterns | 20 min | `exercises/03_streaming/` |
| 4 | Testing with pytest | 20 min | `exercises/04_testing/` |
| 5 | Performance (Locust) | 20 min | `exercises/05_performance/` |
| 6 | Monitoring (Prometheus + Grafana) | 20 min | `docker-compose.yml` |

---

## Project structure

```
workshop/
├── protos/
│   └── chat.proto              ← proto schema (source of truth)
├── chat/
│   ├── server.py               ← gRPC server implementation
│   ├── client.py               ← Typer CLI client
│   ├── main.py                 ← entry point
│   └── generated/              ← auto-generated (run poe generate)
├── tests/
│   ├── conftest.py             ← pytest fixtures
│   ├── test_chat.py            ← integration tests
│   └── locustfile.py           ← load test
├── monitoring/
│   ├── prometheus.yml          ← scrape config
│   └── grafana/                ← dashboards + provisioning
├── exercises/                  ← starter files for each exercise
└── solutions/                  ← complete implementations
```

---

## Monitoring stack

```bash
# Start server + Prometheus + Grafana
docker compose up -d

# Services:
# gRPC server   → localhost:50051
# Prometheus    → localhost:9090
# Grafana       → localhost:3000  (admin / admin)
```

Open Grafana → Dashboards → **gRPC Chat Service** to see:
- Request rate per method
- Latency p50 / p95 / p99
- Error rate

---

## Running tests

```bash
# Run all tests
poe test

# Specific test file
pytest tests/test_chat.py -v

# Specific test
pytest tests/test_chat.py::test_send_message_returns_id_and_ok_status -v
```

---

## gRPC communication patterns

| Pattern | Proto syntax | Use case |
|---------|-------------|----------|
| Unary | `rpc F(Req) returns (Resp)` | Simple request/response |
| Server streaming | `rpc F(Req) returns (stream Resp)` | Feeds, file download |
| Client streaming | `rpc F(stream Req) returns (Resp)` | File upload, bulk insert |
| Bidirectional | `rpc F(stream Req) returns (stream Resp)` | Chat, gaming, IoT |
