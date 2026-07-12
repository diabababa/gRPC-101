"""Solution tests — Exercise 06: deadlines, cancellation, and errors."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import grpc


def _load_deadlines_module():
    module_path = (
        Path(__file__).resolve().parents[2]
        / "solutions"
        / "06_deadlines_cancellation_errors"
        / "deadlines_demo.py"
    )
    spec = importlib.util.spec_from_file_location("deadlines_demo", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_deadline_demo_returns_deadline_exceeded():
    module = _load_deadlines_module()
    code = module.demo_deadline_exceeded()
    assert code == grpc.StatusCode.DEADLINE_EXCEEDED


def test_cancellation_demo_returns_true():
    module = _load_deadlines_module()
    cancelled = module.demo_client_cancellation()
    assert cancelled is True


def test_invalid_argument_demo_returns_invalid_argument(grpc_addr):
    module = _load_deadlines_module()
    module.SOLUTION_SERVER = grpc_addr
    code = module.demo_invalid_argument()
    assert code == grpc.StatusCode.INVALID_ARGUMENT
