import asyncio
import aiohttp
import random

NODES = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002"
]

RESOURCES = ["fileA", "fileB", "fileC"]

async def simulate_activity():
    async with aiohttp.ClientSession() as session:
        while True:
            node = random.choice(NODES)
            resource = random.choice(RESOURCES)
            action = random.choice(["lock", "unlock"])

            try:
                url = f"{node}/{action}"
                async with session.post(url, json={"resource": resource}) as resp:
                    text = await resp.text()
                    print(f"➡️ {node} -> {action.upper()}('{resource}') => {resp.status} {text}")
            except Exception as e:
                print(f"⚠️ Gagal mengirim ke {node}: {e}")

            await asyncio.sleep(random.uniform(1.5, 3.0))  # jeda acak antar request

if __name__ == "__main__":
    asyncio.run(simulate_activity())