"""
Locust load testing for REST API and gRPC API comparison.
"""
from locust import HttpUser, task, between, events
from locust.contrib.fasthttp import FastHttpUser
import json
import random
import time
from datetime import datetime


# Test data
TEST_LOCATIONS = [
    {
        "name": f"Location {i}",
        "latitude": 52.0 + random.uniform(-1, 1),
        "longitude": 21.0 + random.uniform(-1, 1),
        "description": f"Test location {i}",
        "type": random.choice(["restaurant", "hotel", "museum", "park"]),
    }
    for i in range(100)
]


class RESTAPIUser(FastHttpUser):
    """Load testing user for REST API."""

    wait_time = between(1, 3)

    def on_start(self):
        """Seed initial data."""
        # Create some test locations
        for i in range(5):
            self.client.post(
                "/locations",
                json=TEST_LOCATIONS[i],
            )

    @task(40)
    def search_locations(self):
        """Search for locations - 40% of load."""
        lat = 52.0 + random.uniform(-0.5, 0.5)
        lon = 21.0 + random.uniform(-0.5, 0.5)
        self.client.get(
            "/locations/search",
            params={
                "latitude": lat,
                "longitude": lon,
                "radius_km": 10,
                "limit": 50,
            },
        )

    @task(30)
    def get_location(self):
        """Get single location - 30% of load."""
        loc_id = random.randint(1, 5)
        self.client.get(f"/locations/{loc_id}", name="/locations/[id]")

    @task(20)
    def create_location(self):
        """Create location - 20% of load."""
        self.client.post("/locations", json=random.choice(TEST_LOCATIONS))

    @task(5)
    def batch_upload(self):
        """Batch upload locations - 5% of load."""
        locations_batch = random.sample(TEST_LOCATIONS, 10)
        self.client.post("/locations/batch-upload", json=locations_batch)

    @task(5)
    def stream_nearby(self):
        """Stream nearby locations - 5% of load."""
        lat = 52.0 + random.uniform(-0.5, 0.5)
        lon = 21.0 + random.uniform(-0.5, 0.5)
        with self.client.get(
            "/locations/stream/nearby",
            params={"latitude": lat, "longitude": lon, "radius_km": 5},
            stream=True,
        ) as response:
            for line in response.iter_lines():
                if line:
                    pass  # Process SSE events


class RESTAPIHealthCheck(FastHttpUser):
    """Simple health check user."""

    wait_time = between(2, 4)

    @task
    def health_check(self):
        """Check health endpoint."""
        self.client.get("/health")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when test starts."""
    print("\n" + "=" * 50)
    print(f"Test started at {datetime.now()}")
    print("=" * 50)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when test stops."""
    print("\n" + "=" * 50)
    print(f"Test stopped at {datetime.now()}")
    print("=" * 50)
