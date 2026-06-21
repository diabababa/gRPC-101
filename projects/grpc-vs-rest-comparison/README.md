# REST vs gRPC Performance Comparison

Comprehensive performance comparison project between REST (FastAPI async) and gRPC with streaming operations and load testing using Locust.

## Features

- **REST API** with FastAPI async server
- **gRPC Server** with async support
- **4 API Operations**:
  - Unary RPC (request/response)
  - Server streaming
  - Client streaming
  - Bidirectional streaming
- **Performance Testing** with Locust
- **Docker** containerization

## Quick Start

### Prerequisites
- Python 3.14+
- uv package manager
- Docker & Docker Compose

### Setup

```bash
# Install dependencies
uv sync

# Activate environment
source .venv/bin/activate

# Generate gRPC Python files
python -m grpc_tools.protoc -I protos --python_out=shared --grpc_python_out=shared protos/locations.proto
```

### Run REST API

```bash
cd rest-api
uv run uvicorn main:app --reload --port 8000
```

### Run gRPC Server

```bash
cd grpc-api
uv run python server.py
```

### Run Locust Tests

```bash
cd locust-tests
uv run locust -f locustfile.py --host=http://localhost:8000
```

Open http://localhost:8089 for Locust UI

### Docker Compose

```bash
docker-compose up
```

## Project Structure

```
.
├── rest-api/              # FastAPI async server
├── grpc-api/              # gRPC async server
├── shared/                # Shared models, database layer
├── locust-tests/          # Performance tests
├── protos/                # Protobuf definitions
├── pyproject.toml         # Dependencies
├── docker-compose.yml     # Docker orchestration
└── PROJECT_PLAN.md        # Detailed implementation plan
```

## Development

Run tests:
```bash
pytest tests/
```

Format code:
```bash
black .
ruff check . --fix
```

Type checking:
```bash
mypy .
```

## Performance Metrics

- **Throughput** (requests/sec)
- **Latency** (p50, p95, p99)
- **CPU Usage** (%)
- **Memory Usage** (MB)
- **Error Rate** (%)

## Expected Results

gRPC should outperform REST in:
- Throughput (3-5x higher)
- Latency (2-3x lower)
- Resource usage (30-40% lower CPU)
- Streaming efficiency (70% better)

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [gRPC Python Guide](https://grpc.io/docs/languages/python/)
- [Locust Documentation](https://docs.locust.io/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
- [uv Package Manager](https://github.com/astral-sh/uv)

## License

MIT
