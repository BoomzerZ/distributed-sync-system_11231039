import pytest
import asyncio
from src.nodes.lock_manager import LockManager

@pytest.mark.asyncio
async def test_multiple_nodes_scalability():
    nodes = [LockManager(f"node{i}", []) for i in range(5)]
    for i, n in enumerate(nodes):
        await n.request_lock(f"res{i}")
    assert all(n.locks for n in nodes)
