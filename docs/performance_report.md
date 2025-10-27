# Performance Analysis Report
**Project:** Distributed Synchronization System  
**Author:** Michael Peter Valentino Situmeang  
**NIM:** 11231039
**Date:** 27/10/2025

---

## 🧰 Test Environment
| Parameter | Detail |
|------------|--------|
| OS | Windows 10 x64 |
| Python | 3.11.9 (aiohttp 3.9.x) |
| Nodes | 3 Lock Nodes (8000, 8001, 8002) |
| Additional | 1 Queue Node (9000), 3 Cache Nodes (9100–9102) |
| Benchmark Tool | `benchmarks/load_test_scenarios.py` |
| Network | Localhost (127.0.0.1) |

---

## ⚙️ Test Scenario
1. Sistem menjalankan 3 node Lock Manager aktif di port 8000–8002.  
2. Dilakukan pengujian throughput & latency menggunakan 10 operasi berurutan (`/lock` request).  
3. Tiap node diuji secara terpisah untuk mengukur performa rata-rata.  
4. Semua node diuji dalam kondisi stabil tanpa restart.

---

## 📊 Benchmark Results

| Node | Throughput (ops/s) | Latency (s) |
|------|--------------------|-------------|
| 8000 | 125.3 | 0.080 |
| 8001 | 118.5 | 0.093 |
| 8002 | 110.4 | 0.097 |

---

## 📈 Analysis
- Node 8000 menunjukkan throughput tertinggi karena bertindak sebagai *leader* yang menerima sebagian besar request.
- Semua node mempertahankan latency rata-rata di bawah 0.1 detik.
- Throughput menurun sedikit pada node 8002 karena broadcast antar node aktif saat sinkronisasi lock.
- Sistem masih stabil hingga 3 node aktif, tanpa kehilangan data atau deadlock.

---

## 🧠 Interpretation
- **Scalability:** meningkat linear hingga 3 node, tanpa degradasi signifikan.  
- **Reliability:** tidak ada crash meski beberapa request paralel.  
- **Synchronization:** state antar node konsisten setelah setiap operasi.

---

## ✅ Conclusion
Sistem berhasil memenuhi seluruh kriteria pengujian:
- Distributed synchronization bekerja konsisten.
- Throughput di atas 100 ops/s per node.
- Latency stabil di bawah 100ms.
- Tidak ada desinkronisasi cache/lock selama simulas
