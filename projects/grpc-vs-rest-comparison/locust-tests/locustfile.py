"""
Locust load testing configuration and runner.
"""
from locust import HttpUser, task, between, events
from rest_load_test import RESTAPIUser, RESTAPIHealthCheck
import json


class DefaultShape:
    """Default load shape for testing."""

    def __init__(self):
        pass

    def tick(self):
        """Define load progression."""
        run_time = 0
        
        if run_time < 60:
            return (10, 1)  # 10 users, spawn rate 1
        elif run_time < 120:
            return (50, 2)
        elif run_time < 300:
            return (100, 5)
        elif run_time < 360:
            return (500, 10)
        else:
            return None


# Use RESTAPIUser and RESTAPIHealthCheck as default
if __name__ == "__main__":
    import subprocess
    import os

    # Get host from environment or default
    host = os.getenv("REST_HOST", "http://localhost:8000")
    
    # Run locust
    subprocess.run(
        [
            "locust",
            "-f", "rest_load_test.py",
            "--host", host,
            "--users", "100",
            "--spawn-rate", "5",
            "--run-time", "300s",
            "--headless",
            "--print-stats",
            "--csv", "results/rest_results",
        ]
    )
