# REST vs gRPC Performance Comparison - Project Plan

## 📋 Cel Projektu
Porównanie wydajności i charakterystyk REST (FastAPI async) z gRPC na tym samym API, ze szczególnym uwzględnieniem operacji streamingowych i testów obciążeniowych.

---

## 🏗️ Struktura Projektu

```
projects/
├── rest-api/              # FastAPI async server
├── grpc-api/              # gRPC async server
├── shared/                # Shared models, config, database layer
│   ├── models.py
│   ├── config.py
│   └── db.py
├── locust-tests/          # Performance tests
│   ├── rest_load_test.py
│   ├── grpc_load_test.py
│   └── locustfile.py
├── protos/                # Protobuf definitions
│   └── locations.proto
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── Dockerfile.rest
├── Dockerfile.grpc
├── .dockerignore
├── .gitignore
├── README.md
└── PROJECT_PLAN.md
```

---

## 🎯 API Specification

### Główna Idea: Location Management System
Zainspirowany route guide z Twojej wiedzy - zarządzanie lokacjami, wyszukiwanie pobliskich punktów, streaming aktualizacji.

### Operacje API

#### 1. **SearchLocations** (unary - request/response)
- **REST**: `GET /locations/search?latitude=X&longitude=Y&radius=R`
- **gRPC**: `SearchLocationsRequest` → `SearchLocationsReply`
- **Zwraca**: Lista lokacji w promieniu (limit 100)

#### 2. **StreamNearbyLocations** (server streaming)
- **REST**: `GET /locations/stream/nearby?lat=X&lon=Y` (Server-Sent Events)
- **gRPC**: `StreamNearbyRequest` → stream `LocationUpdate`
- **Zwraca**: Continuous stream aktualizacji lokacji

#### 3. **BatchUploadLocations** (client streaming)
- **REST**: `POST /locations/batch-upload` (chunked upload)
- **gRPC**: stream `Location` → `UploadResponse`
- **Załaduj**: Duża ilość lokacji w jednym requestcie

#### 4. **RealTimeLocationSync** (bidirectional streaming)
- **REST**: WebSocket `/ws/location-sync`
- **gRPC**: bidirectional stream `LocationData` ↔ `SyncResponse`
- **Funkcja**: Two-way streaming (client wysyła pozycje, serwer wysyła potwierdzenia + rekomendacje)

---

## 💻 Tech Stack

| Komponent | Technologia | Wersja |
|-----------|-------------|--------|
| Python | Python | 3.14 |
| Package Manager | uv | latest |
| REST Framework | FastAPI | latest |
| ASGI Server | uvicorn | latest |
| gRPC | grpcio | latest |
| Protocol Buffers | protobuf | latest |
| Database (Async) | SQLAlchemy | 2.x |
| DB Driver | asyncpg (PostgreSQL) | latest |
| Performance Testing | Locust | latest |
| Containerization | Docker | latest |
| Async Utilities | asyncio, aiohttp | built-in + latest |

---

## 📅 Implementation Plan

### **Phase 1: Project Setup** (1h)
- [ ] Inicjalizacja uv + pyproject.toml
- [ ] Struktura folderów
- [ ] Konfiguracja .proto files
- [ ] Setup .gitignore, .dockerignore

**Deliverables:**
- `pyproject.toml` z dependencies
- `protos/locations.proto` z message definitions
- Foldery: rest-api/, grpc-api/, shared/, locust-tests/

---

### **Phase 2: Data Models & Database Layer** (2h)
- [ ] SQLAlchemy async models (Location, Review, Rating)
- [ ] Database connection pool (asyncpg)
- [ ] Seed data (JSON lub CSV)
- [ ] CRUD operations (shared layer)

**Deliverables:**
- `shared/models.py` (SQLAlchemy ORM)
- `shared/db.py` (async session, engine setup)
- `shared/config.py` (DB URL, env variables)
- Sample data fixture

---

### **Phase 3: Implement Unary Operations** (2h)

#### REST API
- `GET /locations/search` - search with filters
- `GET /locations/{id}` - get single location
- `POST /locations` - create
- `PUT /locations/{id}` - update
- `DELETE /locations/{id}` - delete

**File**: `rest-api/main.py`

#### gRPC Server
- `SearchLocations` RPC
- `GetLocation` RPC
- `CreateLocation` RPC
- `UpdateLocation` RPC
- `DeleteLocation` RPC

**File**: `grpc-api/server.py`

---

### **Phase 4: Implement Streaming Operations** (3h)

#### REST (Server-Sent Events + WebSocket)
- `GET /locations/stream/nearby` - SSE server streaming
- `WebSocket /ws/location-sync` - bidirectional

**File**: `rest-api/streaming.py`

#### gRPC
- `StreamNearbyLocations` - server streaming
- `BatchUploadLocations` - client streaming  
- `RealTimeLocationSync` - bidirectional streaming

**File**: `grpc-api/server.py`

---

### **Phase 5: Error Handling & Validation** (1h)
- [ ] Input validation (Pydantic + Protobuf)
- [ ] Error responses (REST: HTTP status codes + JSON)
- [ ] gRPC error codes (INVALID_ARGUMENT, NOT_FOUND, itp.)
- [ ] Logging strategy (structured logs)

---

### **Phase 6: Locust Performance Tests** (2h)

#### Test Scenarios
1. **Unary Operations Load**
   - Constant load: 10, 50, 100, 500 users
   - Search queries, CRUD operations
   - Measure: throughput, latency (p50, p95, p99)

2. **Streaming Operations**
   - Server streaming: 50 concurrent streams
   - Client streaming: 100 items per stream
   - Bidirectional: concurrent send/receive

3. **Mixed Workload**
   - 70% unary, 20% server streaming, 10% client streaming
   - Sustained 5 minutes

#### Files
- `locust-tests/rest_load_test.py`
- `locust-tests/grpc_load_test.py`
- `locust-tests/metrics_collector.py` (save results to JSON)

---

### **Phase 7: Docker Setup** (1h)
- [ ] `Dockerfile.rest` - REST API image
- [ ] `Dockerfile.grpc` - gRPC API image
- [ ] `docker-compose.yml` - orchestration
  - REST service (port 8000)
  - gRPC service (port 50051)
  - PostgreSQL (port 5432)
  - Locust master (port 8089)

---

### **Phase 8: Performance Report & Analysis** (1h)
- [ ] Collect metrics from Locust
- [ ] Compare: throughput, latency, memory usage
- [ ] Generate HTML report
- [ ] Document findings

**Deliverables:**
- `PERFORMANCE_REPORT.md`
- `results/` folder z CSV/JSON/charts

---

## 📊 Performance Metrics to Track

### REST API
| Metrika | Narzędzie | Details |
|---------|-----------|---------|
| **Throughput** | Locust | req/sec |
| **Latency** | Locust | p50, p95, p99, avg, min, max (ms) |
| **CPU Usage** | docker stats | % |
| **Memory Usage** | docker stats | MB / % |
| **Error Rate** | Locust | % failed requests |
| **Connection Time** | Locust | ms |

### gRPC API
| Metrika | Narzędzie | Details |
|---------|-----------|---------|
| **Throughput** | Locust + grpcio metrics | req/sec |
| **Latency** | Locust | p50, p95, p99, avg (ms) |
| **CPU Usage** | docker stats | % |
| **Memory Usage** | docker stats | MB / % |
| **Stream Efficiency** | Custom metrics | bytes/sec, frames/sec |
| **Error Rate** | Locust | % failed requests |

---

## 🧪 Locust Test Configuration

```yaml
Load Scenarios:
  1. Ramp Up: 0→100 users, 10 users/sec
  2. Sustained: 100 users, 5 minutes
  3. Spike: 100→500 users instantly, 1 minute
  4. Ramp Down: 500→0 users, 10 users/sec

Request Distribution (Mixed Workload):
  - SearchLocations: 40%
  - StreamNearbyLocations: 30%
  - BatchUploadLocations: 20%
  - RealTimeLocationSync: 10%

Assertions:
  - Response time p95 < 1000ms
  - Error rate < 1%
  - Throughput > 100 req/sec (REST), > 500 req/sec (gRPC)
```

---

## 🐳 Docker Compose Setup

```yaml
version: '3.8'
services:
  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    
  rest-api:
    build:
      context: .
      dockerfile: Dockerfile.rest
    ports:
      - "8000:8000"
    depends_on:
      - db
  
  grpc-api:
    build:
      context: .
      dockerfile: Dockerfile.grpc
    ports:
      - "50051:50051"
    depends_on:
      - db
  
  locust:
    image: locustio/locust
    ports:
      - "8089:8089"
    volumes:
      - ./locust-tests:/home/locust
```

---

## 📈 Expected Outcomes & Hypothesis

### Prognoza wyników (gRPC vs REST)

| Aspekt | gRPC | REST | Uwagi |
|--------|------|------|-------|
| **Throughput** | ~3-5x wyższy | baseline | Binary format vs JSON |
| **Latency (avg)** | ~2-3x niższe | baseline | Less serialization overhead |
| **Latency (p99)** | ~40-50% niższe | baseline | Better connection pooling |
| **Memory per connection** | ~50% mniejsze | baseline | Persistent HTTP/2 |
| **Streaming efficiency** | ~70% lepsze | baseline | Framing vs SSE/WS |
| **CPU usage** | ~30-40% niższe | baseline | Binary parsing efficiency |

### Korzyści gRPC
✅ Wyższa wydajność (throughput, latency)  
✅ Mniejsze zużycie zasobów  
✅ Efektywny streaming (server, client, bidirectional)  
✅ Typed API (Protobuf)  

### Korzyści REST
✅ Prostsze debugowanie (HTTP, JSON)  
✅ Łatwiejsze testowanie (curl, Postman)  
✅ Uniwersalność (każdy browser, każdy klient)  
✅ Większa ekosystem toolingu  

---

## ✅ Checklist - Fazy Implementacji

- [ ] **Phase 1**: Projekt setup
- [ ] **Phase 2**: Database layer
- [ ] **Phase 3**: Unary operations
- [ ] **Phase 4**: Streaming operations
- [ ] **Phase 5**: Error handling
- [ ] **Phase 6**: Load tests
- [ ] **Phase 7**: Docker
- [ ] **Phase 8**: Report

---

## 🚀 Quick Start Commands

```bash
# Setup
uv sync
uv run python -m pytest

# Run REST API
cd rest-api
uv run uvicorn main:app --reload

# Run gRPC Server
cd grpc-api
uv run python server.py

# Run Locust
cd locust-tests
uv run locust -f locustfile.py --host=http://localhost:8000

# Docker Compose
docker-compose up

# Locust UI
# Open http://localhost:8089
```

---

## 📚 Referencje

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [gRPC Python Guide](https://grpc.io/docs/languages/python/)
- [Locust Docs](https://docs.locust.io/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
- [uv Package Manager](https://github.com/astral-sh/uv)

---

**Project Start Date:** 17 May 2026  
**Estimated Duration:** 13 hours total  
**Status:** 🟡 Planning Phase
