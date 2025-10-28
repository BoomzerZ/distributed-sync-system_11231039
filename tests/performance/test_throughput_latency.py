import time
import asyncio
import pytest
from src.nodes.lock_manager import LockManager

@pytest.mark.asyncio
async def test_lock_performance(benchmark):
    node = LockManager("node1", [])
    start = time.time()

    for i in range(100):
        await node.request_lock(f"file_{i}")
        await node.release_lock(f"file_{i}")

    duration = time.time() - start
    ops = 100 / duration
    print(f"Throughput: {ops:.2f} ops/sec")
    assert ops > 50
