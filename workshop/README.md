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
|------|--------------|
| `poe generate-exercises` | Compile `exercises/01_protocol_buffers/chat.proto` → `exercises/generated/` |
| `poe generate-solutions` | Compile `solutions/01_protocol_buffers/chat.proto` → `solutions/generated/` |
| `poe server` | Start gRPC server on port 50051 (exercises) |
| `poe server-solutions` | Start gRPC server on port 50051 (solutions) |
| `poe test-exercises` | Generate + run pytest for exercises |
| `poe test-solutions` | Generate + run pytest for solutions |
| `poe lint` | Ruff linter |
| `poe fmt` | Ruff formatter |

---

## Workshop agenda

| # | Topic | Time | Files |
|---|-------|------|-------|
| 1 | Protocol Buffers | 15 min | `exercises/01_protocol_buffers/` |
| 2 | Service Stub | 10 min | `exercises/02_service_stub/` |
| 3 | Unary Service | 15 min | `exercises/03_unary_service/` |
| 4 | Unary Client | 15 min | `exercises/04_unary_client/` |
| 5 | Streaming Patterns | 20 min | `exercises/05_streaming/` |
| 6 | Monitoring (Prometheus + Grafana) | 20 min | `docker-compose.yml` |

---

## Project structure

```
workshop/
├── exercises/
│   ├── 01_protocol_buffers/    ← Exercise 1: proto schema to complete
│   ├── 02_service_stub/
│   ├── 03_unary_service/
│   ├── 04_unary_client/
│   ├── 05_streaming/
│   ├── generated/              ← auto-generated (run poe generate-exercises)
│   ├── server.py               ← YOUR server — edit this
│   ├── client.py               ← CLI client
│   └── main.py                 ← entry point
├── solutions/                  ← complete reference implementations
├── tests/
│   ├── exercises/              ← one test file per exercise
│   └── solutions/              ← solution test suite
├── infrastructure/
│   ├── Dockerfile.dev
│   └── monitoring/             ← Prometheus + Grafana config
└── docker-compose.yml
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
# Run exercises test suite (generates stubs first)
poe test-exercises

# Run solutions test suite
poe test-solutions

# Run a single test file
poe generate-exercises && pytest tests/exercises/test_03_unary_service.py -v
```

---

## gRPC communication patterns

| Pattern | Proto syntax | Use case |
|---------|-------------|----------|
| Unary | `rpc F(Req) returns (Resp)` | Simple request/response |
| Server streaming | `rpc F(Req) returns (stream Resp)` | Feeds, file download |
| Client streaming | `rpc F(stream Req) returns (Resp)` | File upload, bulk insert |
| Bidirectional | `rpc F(stream Req) returns (stream Resp)` | Chat, gaming, IoT |
