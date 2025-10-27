# Deployment Guide

## Prerequisites
- Python 3.11+
- Docker & Docker Compose
- `pip install -r requirements.txt`

## Manual Run
1. Jalankan 3 node lock:
   ```bash
   python -m src.main --node node1 --port 8000
   python -m src.main --node node2 --port 8001
   python -m src.main --node node3 --port 8002

2. Jalankan queue node:
   python -m src.nodes.queue_node

3. Jalankan cache nodes:
   python -m src.nodes.cache_node

## Docker Run
cd docker
docker compose up --build

## Testing
Lock test: curl http://127.0.0.1:8000/lock

Queue test: curl http://127.0.0.1:9000/queue

Cache test: curl http://127.0.0.1:9100/cache

