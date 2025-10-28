import pytest
import asyncio
from src.nodes.lock_manager import LockManager

@pytest.mark.asyncio
async def test_lock_sync_between_nodes(monkeypatch):
    node1 = LockManager("node1", ["http://127.0.0.1:8001"])
    node2 = LockManager("node2", ["http://127.0.0.1:8000"])

    await node1.request_lock("shared_file")
    assert "shared_file" in node1.locks