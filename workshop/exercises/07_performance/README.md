# Exercise 5: Performance with Locust (20 min)

## Goal

Write a Locust load test that simulates concurrent users hitting the gRPC Chat service, then interpret the results.

## Background

Locust doesn't have built-in gRPC support, so we implement `GrpcUser`:
- Creates a gRPC channel in `on_start`
- Wraps each call with `events.request.fire(...)` to record timing and failures

## Your task

Open `locustfile_starter.py` and implement:

### Task 1 — `send_message` task (weight 3)

Call `self._stub.SendMessage(...)` inside `self._call("SendMessage", ...)`.

### Task 2 — `get_history` task (weight 1)

Server streaming returns an iterator. Wrap it so Locust can time it:
```python
self._call(
    "GetHistory",
    lambda req: list(self._stub.GetHistory(req)),  # consume the iterator
    chat_pb2.HistoryRequest(room_id="perf-room", limit=5),
)
```

### Bonus — `send_bulk` task (weight 1)

Send a client-streaming batch of 5 messages.

## Run the test

```bash
# Terminal 1 — start the server
poe server

# Terminal 2 — start Locust (web UI)
locust -f exercises/05_performance/locustfile_starter.py
# Open http://localhost:8089
# Set: users=50, spawn rate=5, host=localhost (ignored for gRPC)

# Or headless
locust -f exercises/05_performance/locustfile_starter.py \
  --headless --users 50 --spawn-rate 5 --run-time 30s
```

## Questions to answer

1. What is the max stable RPS before failures appear?
2. What is the p95 latency at 50 concurrent users?
3. Which method (`SendMessage` / `GetHistory` / `SendBulkMessages`) is slowest? Why?
4. What happens if you set `wait_time = constant(0)`?

## Solution

`solutions/05_performance/locustfile.py`
