# Project Setup

## TODO: add QR code

clone repository: <strong>github.com/kamilkulig/grpc-101</strong>


```bash
# Clone & enter workshop
cd workshop

# run test-exercises
docker compose run --rm workshop poe test-solutions
docker compose run --rm workshop poe test-exercises

# Or create virtualenv and install deps and run
uv sync
source .venv/bin/activate
poe test-exercises
poe test-solutions
```
