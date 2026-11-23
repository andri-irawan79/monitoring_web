# Migrasi basis data

| Berkas | Untuk | Catatan |
|---|---|---|
| `000_base_schema.sql` | **Instalasi baru** (basis data kosong) | users, fase_pertumbuhan (+seed 5 fase), monitoring, rekomendasi, arsip varietas. Idempoten. |
| `001_remove_varietas_master.sql` | Basis data **lama** yang masih punya master varietas | Jangan dijalankan pada instalasi baru. |
| `002_fis1_fis2_multi_fertilizer.sql` | Semua basis data | Kolom FIS-1/FIS-2, `fuzzy_trace`, tabel `rekomendasi_detail` |
| `003_add_soil_moisture.sql` | Semua basis data | Kolom `monitoring.soil_moisture` |

Instalasi baru: `000 -> 002 -> 003` (docker compose melakukannya otomatis). Basis data lama: ambil cadangan (`pg_dump -Fc`), lalu `001` (bila perlu) -> `002` -> `003`.

**Satu catatan tentang duplikasi.** `main.py` juga menjalankan DDL idempoten yang setara dengan 002/003 saat startup (jaring pengaman untuk basis data yang lupa dimigrasi).
Keduanya dijaga agar tidak berbeda oleh `backend/tests/test_migrasi_konsisten.py`. Bila menambah kolom, ubah **kedua** tempat dan jalankan pytest.
