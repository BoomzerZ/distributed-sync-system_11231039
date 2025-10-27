import asyncio
from aiohttp import web, ClientSession

class CacheNode:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.cache = {}  # {key: (value, state)}
        self.app = web.Application()
        self.app.router.add_post('/put', self.put)
        self.app.router.add_get('/get/{key}', self.get)
        self.app.router.add_post('/invalidate', self.invalidate)
        self.app.router.add_get('/cache', self.get_cache)

    async def broadcast_invalidate(self, key):
        """Kirim pesan invalidasi ke node lain"""
        async with ClientSession() as session:
            for peer in self.peers:
                try:
                    await session.post(f"{peer}/invalidate", json={"key": key})
                    print(f"[{self.node_id}] 📨 Invalidate '{key}' dikirim ke {peer}")
                except Exception as e:
                    print(f"[{self.node_id}] ⚠️ Gagal kirim ke {peer}: {e}")

    async def put(self, request):
        data = await request.json()
        key, value = data.get("key"), data.get("value")

        # Update lokal
        self.cache[key] = (value, "M")
        print(f"[{self.node_id}] ✏️ Set '{key}' = '{value}' (Modified)")

        # Broadcast invalidation
        await self.broadcast_invalidate(key)
        return web.json_response({"message": f"{key} disimpan di {self.node_id}"})

    async def get(self, request):
        key = request.match_info["key"]
        if key in self.cache and self.cache[key][1] != "I":
            value, state = self.cache[key]
            print(f"[{self.node_id}] 📦 Get '{key}' -> '{value}' ({state})")
            return web.json_response({"key": key, "value": value, "state": state})
        else:
            print(f"[{self.node_id}] ⚠️ Cache miss untuk '{key}'")
            return web.json_response({"key": key, "value": None, "state": "MISS"})

    async def invalidate(self, request):
        data = await request.json()
        key = data.get("key")
        if key in self.cache:
            self.cache[key] = (self.cache[key][0], "I")
            print(f"[{self.node_id}] ❌ Invalidate '{key}' (Invalid)")
        return web.json_response({"message": f"{key} invalidated di {self.node_id}"})

    async def get_cache(self, request):
        return web.json_response({
            "cache": {k: {"value": v, "state": s} for k, (v, s) in self.cache.items()}
        })

    def run(self, host="127.0.0.1", port=9100):
        print(f"🚀 Cache Node {self.node_id} aktif di http://{host}:{port}")
        web.run_app(self.app, host=host, port=port)


if __name__ == "__main__":
    peers = ["http://127.0.0.1:9100", "http://127.0.0.1:9101"]
    node = CacheNode("node3", peers)
    node.run(host="127.0.0.1", port=9102)
