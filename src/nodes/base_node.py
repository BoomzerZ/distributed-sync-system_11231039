from aiohttp import web
from src.nodes.lock_manager import LockManager
from prometheus_client import Counter, Gauge, start_http_server

class BaseNode:
    def __init__(self, node_id, host, port, peers):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.app = web.Application()
        self.manager = LockManager(node_id, peers)

         # Metrics
        self.lock_requests = Counter('lock_requests_total', 'Total number of lock requests', ['node'])
        self.unlock_requests = Counter('unlock_requests_total', 'Total number of unlock requests', ['node'])
        self.active_locks = Gauge('active_locks', 'Number of active locks', ['node'])

        # Route definitions
        self.app.add_routes([
            web.get('/health', self.health_check),
            web.post('/lock', self.handle_lock),
            web.post('/unlock', self.handle_unlock),
            web.post('/sync', self.handle_sync),
            web.get('/locks', self.get_locks)
        ])

    async def health_check(self, request):
        return web.json_response({"status": "ok", "node": self.node_id})

    async def handle_lock(self, request):
        data = await request.json()
        await self.manager.request_lock(data["resource"])
        return web.json_response({"message": f"{self.node_id} processed lock"})

    async def handle_unlock(self, request):
        data = await request.json()
        await self.manager.release_lock(data["resource"])
        return web.json_response({"message": f"{self.node_id} processed unlock"})

    async def handle_sync(self, request):
        data = await request.json()
        self.manager.sync_state(data["action"], data["resource"], data["owner"])
        return web.json_response({"message": f"{self.node_id} synced {data['action']}"})

    async def get_locks(self, request):
        """Menampilkan semua resource yang sedang dikunci"""
        return web.json_response({"locks": self.manager.locks})

    def run(self):
        start_http_server(self.port + 100)
        print(f"📊 Metrics running at http://127.0.0.1:{self.port + 100}/metrics")
        web.run_app(self.app, host=self.host, port=self.port)
