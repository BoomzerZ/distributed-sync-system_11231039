import asyncio
import hashlib
from aiohttp import web, ClientSession

class DistributedQueue:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.queue = []
        self.app = web.Application()
        self.app.router.add_post('/enqueue', self.enqueue)
        self.app.router.add_get('/dequeue', self.dequeue)
        self.app.router.add_get('/queue', self.get_queue)

    def get_hash(self, item):
        """Membuat hash untuk menentukan node tujuan (simulasi consistent hashing)"""
        return int(hashlib.sha1(item.encode()).hexdigest(), 16) % len(self.peers)

    async def enqueue(self, request):
        data = await request.json()
        message = data.get("message")

        if not message:
            return web.json_response({"error": "message kosong"}, status=400)

        target_index = self.get_hash(message)
        target_node = self.peers[target_index]

        # Jika message untuk node ini, tambahkan lokal
        if target_node.endswith(f":{9000 + int(self.node_id[-1]) - 1}"):
            self.queue.append(message)
            print(f"[{self.node_id}] 📥 Menambahkan pesan '{message}' ke antrian lokal.")
        else:
            # Forward ke node lain
            async with ClientSession() as session:
                try:
                    await session.post(f"{target_node}/enqueue", json={"message": message})
                    print(f"[{self.node_id}] 🔁 Meneruskan '{message}' ke {target_node}")
                except Exception as e:
                    print(f"[{self.node_id}] ⚠️ Gagal mengirim ke {target_node}: {e}")

        return web.json_response({"status": "queued", "message": message})

    async def dequeue(self, request):
        if self.queue:
            message = self.queue.pop(0)
            print(f"[{self.node_id}] 📤 Mengambil pesan '{message}' dari antrian.")
            return web.json_response({"message": message})
        else:
            return web.json_response({"message": None})

    async def get_queue(self, request):
        return web.json_response({"queue": self.queue})

    def run(self, host="127.0.0.1", port=9000):
        print(f"🚀 Queue Node {self.node_id} aktif di http://{host}:{port}")
        web.run_app(self.app, host=host, port=port)


if __name__ == "__main__":
    node = DistributedQueue("node1", ["http://127.0.0.1:9000"])
    node.run(host="127.0.0.1", port=9000)
