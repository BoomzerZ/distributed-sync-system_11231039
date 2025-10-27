# Distributed Synchronization System - Architecture

## Overview
Sistem ini terdiri dari tiga subsistem utama:
1. **Distributed Lock Manager** - sinkronisasi resource antar node menggunakan Raft-like consensus.
2. **Distributed Queue System** - antrian terdistribusi dengan consistent hashing.
3. **Distributed Cache Coherence** - sinkronisasi cache antar node dengan protokol MESI sederhana.

## Node Structure
Setiap node berjalan dengan `aiohttp` dan memiliki endpoint:
- `/lock`, `/unlock`, `/sync` — untuk manajemen kunci.
- `/enqueue`, `/dequeue`, `/queue` — untuk sistem antrian.
- `/put`, `/get/{key}`, `/invalidate`, `/cache` — untuk cache coherence.

## Communication Flow
- Antar node berkomunikasi via HTTP async menggunakan `aiohttp.ClientSession`.
- Lock dan cache menggunakan mekanisme broadcast untuk menjaga konsistensi.
- Queue menggunakan consistent hashing untuk membagi pesan ke node target.

## Technology Stack
- **Python 3.11**
- **aiohttp + asyncio**
- **Redis (optional)** untuk state persistence
- **Docker + Compose** untuk deployment multi-node
- **Locust / Benchmark Script** untuk uji performa
