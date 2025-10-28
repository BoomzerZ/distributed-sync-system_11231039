import pytest
from src.nodes.cache_node import CacheNode

@pytest.mark.asyncio
async def test_write_and_read():
    node = CacheNode("node1", "127.0.0.1", 9100, [])
    await node.handle_write(type("req", (), {"json": lambda: {"key": "x", "value": "1"}})())
    assert "x" in node.cache
