import asyncio
import aiohttp
import time

URLS = [
    "http://127.0.0.1:8000/lock",
    "http://127.0.0.1:8001/lock",
    "http://127.0.0.1:8002/lock"
]

async def test_throughput(session, url, resource):
    start = time.perf_counter()
    for _ in range(10):
        await session.post(url, json={"resource": resource, "owner": "test"})
    end = time.perf_counter()
    duration = end - start
    return 10 / duration  # ops per detik

async def test_latency(session, url, resource):
    start = time.perf_counter()
    await session.post(url, json={"resource": resource, "owner": "test"})
    end = time.perf_counter()
    return end - start

async def main():
    async with aiohttp.ClientSession() as session:
        results = []
        for url in URLS:
            thr = await test_throughput(session, url, "resA")
            lat = await test_latency(session, url, "resB")
            results.append((url, thr, lat))

        print("\n📊 Hasil Benchmark:")
        print("===========================================")
        print("| Node | Throughput (ops/s) | Latency (s) |")
        print("===========================================")
        for url, thr, lat in results:
            print(f"| {url.split(':')[-1]} | {thr:17.2f} | {lat:10.5f} |")
        print("===========================================")

if __name__ == "__main__":
    asyncio.run(main())
