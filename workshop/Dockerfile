FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml .python-version ./
RUN uv sync --no-dev --frozen || uv sync --no-dev

COPY protos/ protos/
COPY chat/ chat/

RUN uv run python -m grpc_tools.protoc \
    -I protos \
    --python_out=chat/generated \
    --grpc_python_out=chat/generated \
    protos/chat.proto

EXPOSE 50051 8000

CMD ["uv", "run", "python", "-m", "chat.main", "server"]
