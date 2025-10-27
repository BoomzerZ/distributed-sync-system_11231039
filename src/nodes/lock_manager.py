import asyncio
import aiohttp

class LockManager:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.locks = {}

    async def request_lock(self, resource):
        if resource in self.locks:
            print(f"[{self.node_id}] ❌ Resource '{resource}' sudah dikunci oleh {self.locks[resource]}")
            return False

        # Kunci resource ini
        self.locks[resource] = self.node_id
        print(f"[{self.node_id}] 🔒 Mengunci '{resource}'")

        # Broadcast ke node lain
        await self.broadcast("lock", resource)
        return True

    async def release_lock(self, resource):
        if resource not in self.locks or self.locks[resource] != self.node_id:
            print(f"[{self.node_id}] ⚠️ Tidak bisa melepas lock '{resource}' (bukan pemilik)")
            return False

        del self.locks[resource]
        print(f"[{self.node_id}] 🔓 Melepas lock '{resource}'")

        # Broadcast ke node lain
        await self.broadcast("unlock", resource)
        return True

    async def broadcast(self, action, resource):
        async with aiohttp.ClientSession() as session:
            for peer in self.peers:
                try:
                    await session.post(f"{peer}/sync", json={
                        "action": action,
                        "resource": resource,
                        "owner": self.node_id
                    })
                    print(f"[{self.node_id}] 📡 Broadcast '{action}' ke {peer}")
                except Exception as e:
                    print(f"[{self.node_id}] ⚠️ Gagal broadcast ke {peer}: {e}")

    def sync_state(self, action, resource, owner):
        if action == "lock":
            self.locks[resource] = owner
        elif action == "unlock":
            self.locks.pop(resource, None)
        print(f"[{self.node_id}] 🔁 Sync {action} untuk '{resource}' oleh {owner}")
