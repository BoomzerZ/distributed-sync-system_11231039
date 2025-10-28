import pytest
from src.nodes.lock_manager import LockManager

@pytest.mark.asyncio
async def test_broadcast_method(monkeypatch):
    node = LockManager("node1", ["http://fake-node"])
    called = []

    async def mock_post(url, json):
        called.append(url)
    monkeypatch.setattr("aiohttp.ClientSession.post", mock_post)

    await node.broadcast("lock", "fileA")
    assert called
