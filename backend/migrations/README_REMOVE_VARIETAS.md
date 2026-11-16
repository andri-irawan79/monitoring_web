# Migrasi Alternatif B: menghapus master varietas

## Tujuan

Ruang lingkup aplikasi telah ditetapkan khusus untuk tanaman durian varietas Montong. Karena itu, varietas tidak lagi dikelola sebagai master data, bukan variabel Fuzzy Tsukamoto, dan tidak menjadi faktor koreksi dosis.

Perubahan:
- Hapus kolom `rekomendasi.varietas_id`.
- Hapus endpoint `/varietas/`.
- Hapus tabel master `varietas`.
- Pertahankan informasi varietas lama di `rekomendasi_varietas_archive` sebagai arsip audit.
- Gunakan konstanta aplikasi `PLANT_VARIETY = "Montong"` dan `PLANT_DISPLAY_NAME = "Durian Montong"`.

## Prosedur database

1. Hentikan backend, frontend, dan simulator.
2. Buat backup penuh PostgreSQL:
   `pg_dump -Fc -d NAMA_DATABASE -f before_remove_varietas.dump`
3. Pastikan database target benar.
4. Jalankan:
   `psql -d NAMA_DATABASE -v ON_ERROR_STOP=1 -f backend/migrations/001_remove_varietas_master.sql`
5. Periksa tabel arsip dan pastikan mapping rekomendasi lama tersimpan.
6. Pastikan tabel `varietas` dan kolom `rekomendasi.varietas_id` sudah tidak ada.
7. Jalankan backend dan uji endpoint rekomendasi, riwayat, dan ekspor CSV.

Migrasi menggunakan transaksi. Jika ada tabel lain yang masih mempunyai foreign key ke `varietas`, skrip membatalkan perubahan; jangan mengganti dengan `DROP ... CASCADE` sebelum relasi lain diperiksa.

## Struktur rekomendasi sesudah migrasi

Tabel `rekomendasi` menyimpan:
- `id`
- `monitoring_id`
- `fase_id`
- `jenis_pupuk`
- `dosis`
- `kategori`
- `created_at`

Nama Durian Montong untuk hasil, riwayat, dan CSV diisi dari konfigurasi aplikasi, tanpa JOIN ke tabel varietas.

## Perubahan API dan frontend

- Endpoint `/varietas/` dihapus.
- Fungsi `getVarietas()` dihapus dari masterService.
- Form rekomendasi tetap menampilkan Durian Montong sebagai informasi tetap.
- Endpoint latest/history/export menampilkan nilai tetap Durian Montong dari konfigurasi backend.

## Catatan

Tabel arsip bukan bagian dari transaksi rekomendasi aktif dan tidak dipetakan ke ORM. Jangan menghapus tabel arsip sebelum riwayat lama tidak lagi diperlukan.
