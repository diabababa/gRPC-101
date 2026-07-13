# Project Setup

![alt text](assets/qrcode_github.com.png)

```bash
git clone https://github.com/KuligKamil/grpc-workshop/
```


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
