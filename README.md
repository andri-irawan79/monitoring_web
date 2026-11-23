# Monitoring Kondisi Tanah dan Rekomendasi Pemupukan Durian Monthong (fuzzy Tsukamoto)

Aplikasi web skripsi: simulator Python mengirim data tanah ke API FastAPI melalui HTTP REST; backend menghitung rekomendasi
pemupukan dengan fuzzy Tsukamoto (BAB III subbab 3.6); frontend Vue menampilkan monitoring, rekomendasi, dan riwayat.

```
backend/    FastAPI, SQLAlchemy, PostgreSQL; fuzzy/ = mesin fuzzy v2; simulator/; migrations/; tests/
frontend/   Vue 3, Vite, Tailwind, Axios
riset/      bukti penelitian: tabel acuan TERKUNCI (sha256), skenario uji, data simulasi, implementasi acuan, baseline mesin lama
docs/       (tambahkan diagram dan catatan desain di sini)
```

## Menjalankan (Docker)
```bash
cp .env.example .env                       # konfigurasi Docker Compose
cp backend/.env.example backend/.env        # konfigurasi backend; samakan DB_PASSWORD pada kedua file
# Ganti JWT_SECRET_KEY dan SIMULATOR_API_KEY sebelum menjalankan aplikasi.
docker compose up -d --build                # PostgreSQL (skema 000, 002, 003 otomatis) + backend di :8000
cd frontend && npm ci && npm run dev        # http://localhost:5173
```
PostgreSQL host dipetakan ke port 5433 agar tidak bertabrakan dengan PostgreSQL lokal di 5432. Mengulang dari nol: `docker compose down -v` (menghapus volume database Docker; jangan jalankan bila data masih diperlukan). Basis data lama (sudah berisi data): lihat `backend/migrations/README.md`.

## Menjalankan tanpa Docker
```bash
cd backend && pip install -r requirements-dev.txt
# siapkan PostgreSQL lalu jalankan migrations/000 -> 002 -> 003 dengan psql, isi backend/.env
uvicorn main:app --reload
```

## Pengujian
```bash
cd backend && pytest -q
```
Mencakup: contoh hitung manual, **paritas** dengan implementasi acuan (600 baris buah x 5 fase x profil A dan B), **tabel acuan terkunci**
(sidik jari dan ambang >= 90% pada 450 pengamatan), **pembanding crisp**, **uji monotonik** (toleransi 5 poin persen), **uji kewajaran**
dosis tahunan, validasi masukan monitoring, dan konsistensi DDL `main.py` dengan migrasi. CI (`.github/workflows/ci.yml`) menjalankannya
beserta migrasi pada PostgreSQL sungguhan dan build frontend.

## Aturan penting
- `riset/tabel_acuan_v1.json` dan `.sha256` **terkunci**; perubahan = versi baru dengan alasan tertulis (uji akan gagal bila berkas diubah).
- Parameter fuzzy ada di `backend/fuzzy/parameter.py` (profil A kuartil data buah; profil B batas pedoman uji tanah untuk uji sensitivitas).
- Nilai Dolomit/Belerang masih indikatif (belum bersumber); lihat `parameter_warnings` pada respons rekomendasi.
- Ganti semua nilai rahasia sebelum penerapan; gunakan HTTPS.
