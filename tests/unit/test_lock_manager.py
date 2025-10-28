import pytest
import asyncio
from src.nodes.lock_manager import LockManager

@pytest.mark.asyncio
async def test_request_and_release_lock():
    manager = LockManager("node1", [])
    result = await manager.request_lock("fileA")
    assert result is True
    assert "fileA" in manager.locks

    released = await manager.release_lock("fileA")
    assert released is True
    assert "fileA" not in manager.locks