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
- `/auth/change-password`: mengubah kata sandi setelah memverifikasi kata sandi saat ini. Kata sandi baru minimal 8 karakter dan maksimal 128 karakter.
- `/logout`: dilakukan di frontend dengan menghapus token sesi.

Token akses ditandatangani menggunakan HMAC-SHA256 dan berlaku sesuai TOKEN_TTL_SECONDS (bawaan 8 jam). Kata sandi disimpan sebagai hash PBKDF2-HMAC-SHA256, bukan teks asli. Token disimpan pada sessionStorage browser. Setelah kata sandi berhasil diubah, backend menaikkan `auth_version` akun dan menerbitkan token baru untuk browser yang sedang digunakan. Token sesi lain dengan versi sebelumnya otomatis ditolak pada permintaan API berikutnya. Kolom `auth_version` ditambahkan otomatis saat startup backend; akun dan data yang sudah ada tetap dipertahankan.

Endpoint dashboard, master data, monitoring (GET), dan rekomendasi memerlukan header `Authorization: Bearer <token>`. Endpoint penerimaan data simulasi `POST /monitoring/` memakai header `X-Simulator-Key` dan ID sesi yang valid. Sesi tersebut telah dibuat dengan identitas akun melalui login website atau login Git Bash, sehingga setiap record memperoleh pemilik dari sesi di database.

## Batasan fitur autentikasi

Implementasi ini mencakup pendaftaran, masuk, verifikasi sesi, ubah kata sandi, dan keluar. Belum mencakup pembagian role/hak akses bertingkat, verifikasi email, reset kata sandi melalui email, autentikasi multifaktor, maupun pembatasan percobaan masuk (rate limiting). Untuk deployment publik, gunakan HTTPS dan secret acak yang kuat serta pertimbangkan kontrol tambahan tersebut.


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

Sebelum membuat sesi, skrip meminta email dan kata sandi akun untuk login ke API. Token digunakan untuk membuat sesi atas nama akun tersebut dan tidak menyimpan kata sandi. Setelah sesi berhasil dibuat, skrip mengirim data dengan ID sesi. Tekan `Ctrl+C` pada terminal untuk menghentikan sesi sebelum seluruh data dikirim. Skrip menggunakan `Crop_recommendationV2.csv` bila file tersebut tersedia; jika tidak, skrip menggunakan `Crop_recommendation.csv` yang ada di repository. Nama/lokasi file dapat diatur melalui `SIMULATOR_DATASET_PATH` pada `.env`.

### Aturan hitungan sesi

- Setiap sesi baru memiliki penghitung sendiri, dimulai dari `0/365`.
- Setiap record dikirim dengan ID sesi dan nomor urut, sehingga pengiriman ulang record yang sama tidak menambah hitungan dua kali.
- Hanya satu sesi yang boleh aktif untuk setiap akun. Dua akun berbeda dapat menjalankan sesi masing-masing tanpa berbagi penghitung.
- Riwayat monitoring dan sesi sebelumnya tidak dihapus ketika sesi baru dimulai.
- Indikator penerimaan data memakai `SIMULATOR_STATUS_TIMEOUT_SECONDS` (bawaan 8 detik). Sesi baru ditandai gagal jika tidak menerima data melebihi `SIMULATOR_SESSION_TIMEOUT_SECONDS` (bawaan 45 detik), agar proses retry pengiriman tidak terlalu cepat dianggap gagal. Interval kirim bawaan adalah 2 detik melalui `SIMULATOR_INTERVAL_SECONDS`.

Skema `simulation_sessions` dan kolom penghubung pada `monitoring` disiapkan secara idempoten saat backend mulai. Struktur ini menambahkan kolom nullable dan tidak menghapus record monitoring lama. Skrip SQL cadangan tersedia pada `backend/migration_simulation_sessions.sql` dan `backend/migration_user_data_isolation.sql` untuk lingkungan yang melakukan migrasi database secara manual. Jalankan keduanya setelah membuat cadangan database.


## Pemisahan data antar akun

Setiap data monitoring, sesi simulasi, dan rekomendasi baru dikaitkan dengan akun yang sedang masuk. Dashboard, riwayat monitoring, riwayat rekomendasi, penghapusan, dan ekspor CSV hanya menampilkan data milik akun tersebut.

Untuk menjalankan simulator dari Git Bash, skrip meminta email dan kata sandi akun terlebih dahulu. Kredensial digunakan untuk memperoleh token login dan tidak disimpan oleh skrip. Sesi yang dibuat dari website otomatis menggunakan akun yang sedang masuk.

Kolom kepemilikan ditambahkan secara nullable agar record historis tetap tersimpan tanpa dihapus. Record lama yang belum memiliki pemilik tidak ditampilkan kepada akun mana pun sampai pemiliknya ditetapkan secara eksplisit. Ini mencegah data lama diberikan kepada akun yang salah. Cadangkan database sebelum migrasi pertama.


### Mengaitkan data historis yang sudah ada (opsional)

Record yang dibuat sebelum fitur pemisahan akun belum memiliki informasi pemilik. Record tersebut tidak dihapus, tetapi juga tidak ditampilkan kepada akun mana pun sampai pemilik ditentukan. Jangan menjalankan langkah ini sebelum memastikan akun mana yang seharusnya memiliki seluruh data lama.

1. Lihat ID akun di PostgreSQL:

```sql
SELECT id, full_name, email
FROM users
ORDER BY id;
```

2. Ganti angka `<ID_AKUN_PEMILIK>` dengan ID akun yang memang memiliki data historis tersebut, lalu jalankan:

```sql
UPDATE monitoring
SET user_id = <ID_AKUN_PEMILIK>
WHERE user_id IS NULL;

UPDATE simulation_sessions
SET user_id = <ID_AKUN_PEMILIK>
WHERE user_id IS NULL;

UPDATE rekomendasi r
SET user_id = m.user_id
FROM monitoring m
WHERE r.monitoring_id = m.id
  AND r.user_id IS NULL
  AND m.user_id IS NOT NULL;
```

Karena data historis sebelumnya tersimpan bersama tanpa identitas akun, proses ini mengaitkan seluruh record monitoring lama yang belum memiliki pemilik ke satu akun yang dipilih. Akun lain tidak akan melihat record tersebut.
