import pytest
from src.nodes.queue_node import DistributedQueue

@pytest.mark.asyncio
async def test_enqueue_and_dequeue():
    node = DistributedQueue("node1", [])
    await node.enqueue({"message": "Halo Dunia"})
    assert len(node.queue) == 1

    msg = node.queue.pop(0)
    assert msg["message"] == "Halo Dunia"
