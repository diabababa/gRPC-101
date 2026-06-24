"""Exercise 05 — Performance Testing.

Verify the service handles concurrent load without errors and within latency limits.
Run: poe test-exercises
"""
import pytest
from concurrent.futures import ThreadPoolExecutor

import grpc

from exercises.generated import chat_pb2, chat_pb2_grpc


def test_service_handles_concurrent_requests(grpc_addr):
    # TODO: create a function that sends one message using a fresh channel
    # TODO: use ThreadPoolExecutor(max_workers=10) to send 50 requests concurrently
    # TODO: assert no errors occurred
    pytest.fail("Implement this test")


def test_service_responds_within_time_limit(stub):
    # TODO: measure time to send 30 sequential messages
    # TODO: assert total time < reasonable limit (hint: 500ms per message is too slow)
    pytest.fail("Implement this test")
