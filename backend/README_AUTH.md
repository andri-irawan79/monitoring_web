# Autentikasi Pengguna

Fitur autentikasi menyediakan pendaftaran akun, masuk, sesi akses, dan keluar.

## Konfigurasi backend

1. Salin `.env.example` menjadi `.env` di folder `backend`.
2. Isi DB_HOST, DB_PORT, DB_NAME, DB_USER, dan DB_PASSWORD sesuai PostgreSQL lokal.
3. Ganti JWT_SECRET_KEY dan SIMULATOR_API_KEY dengan nilai acak yang berbeda. Jangan mengunggah file `.env` ke Git.
4. Jalankan backend dari folder `backend`:

```bash
uvicorn main:app --reload
```

Tabel `users` dibuat otomatis saat aplikasi mulai apabila tabel tersebut belum tersedia. Jika basis data sudah memiliki tabel `users` lama dengan kolom seperti `username`, `password`, atau `role`, aplikasi menghentikan proses startup dengan pesan migrasi. Cadangkan data terlebih dahulu, lalu migrasikan atau ubah nama tabel lama; pembuatan tabel otomatis tidak mengubah skema tabel yang sudah ada.

## Konfigurasi frontend

Frontend menggunakan `VITE_API_URL` jika tersedia; nilai bawaan adalah `http://127.0.0.1:8000`.

Jalankan frontend:

```bash
npm install
npm run dev
```

## Alur pengguna

- `/register`: membuat akun dengan nama lengkap, email, dan kata sandi minimal 8 karakter.
- `/login`: memverifikasi email dan kata sandi, lalu menerima access token.
- `/auth/me`: memeriksa identitas akun yang sedang masuk.
- `/logout`: dilakukan di frontend dengan menghapus token sesi.

Token akses ditandatangani menggunakan HMAC-SHA256 dan berlaku sesuai TOKEN_TTL_SECONDS (bawaan 8 jam). Kata sandi disimpan sebagai hash PBKDF2-HMAC-SHA256, bukan teks asli. Token disimpan pada sessionStorage browser.

Endpoint dashboard, master data, monitoring (GET), dan rekomendasi memerlukan header `Authorization: Bearer <token>`. Endpoint penerimaan data simulasi `POST /monitoring/` tidak memakai token pengguna, tetapi memerlukan header `X-Simulator-Key` yang harus sama dengan SIMULATOR_API_KEY di backend dan simulator.

## Batasan fitur autentikasi

Implementasi ini mencakup pendaftaran, masuk, verifikasi sesi, dan keluar. Belum mencakup pembagian role/hak akses bertingkat, verifikasi email, reset kata sandi, autentikasi multifaktor, maupun pembatasan percobaan masuk (rate limiting). Untuk deployment publik, gunakan HTTPS dan secret acak yang kuat serta pertimbangkan kontrol tambahan tersebut.


## Kontrol simulasi dan progres per sesi

Simulator dapat dijalankan melalui dua cara. Jalankan backend terlebih dahulu dan pastikan `SIMULATOR_API_KEY` pada file `.env` sama dengan kunci yang dipakai skrip.

### 1. Melalui website

Masuk ke website, lalu gunakan bagian **Kontrol simulasi** pada sidebar. Pilih **Website**, kemudian tekan **Mulai dari website**. Backend menjalankan `backend/simulator/simulator.py` sebagai proses Python dan menyimpan output proses pada `backend/logs/simulator-<session-id>.log`.

Tombol **Hentikan simulasi** hanya menghentikan proses yang dimulai oleh backend website tersebut.

### 2. Melalui Git Bash

Jalankan perintah berikut dari folder utama repository:

```bash
python backend/simulator/simulator.py
```

Skrip akan membuat sesi baru secara otomatis. Tekan `Ctrl+C` pada terminal untuk menghentikan sesi sebelum seluruh data dikirim.

### Aturan hitungan sesi

- Setiap sesi baru memiliki penghitung sendiri, dimulai dari `0/365`.
- Setiap record dikirim dengan ID sesi dan nomor urut, sehingga pengiriman ulang record yang sama tidak menambah hitungan dua kali.
- Hanya satu sesi yang boleh aktif pada satu waktu. Sesi website dan Git Bash tidak dapat berjalan bersamaan.
- Riwayat monitoring dan sesi sebelumnya tidak dihapus ketika sesi baru dimulai.
- Status sesi yang tidak menerima data melebihi `SIMULATOR_STATUS_TIMEOUT_SECONDS` (bawaan 8 detik) akan ditandai gagal saat status diperiksa. Interval kirim bawaan adalah 2 detik melalui `SIMULATOR_INTERVAL_SECONDS`.

Skema `simulation_sessions` dan kolom penghubung pada `monitoring` disiapkan secara idempoten saat backend mulai. Struktur ini menambahkan kolom nullable dan tidak menghapus record monitoring lama. Skrip SQL cadangan tersedia pada `backend/migration_simulation_sessions.sql` untuk lingkungan yang melakukan migrasi database secara manual.
