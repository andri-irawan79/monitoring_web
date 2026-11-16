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
