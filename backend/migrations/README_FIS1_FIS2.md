# Migrasi FIS-1 + FIS-2 dan rekomendasi multi-pupuk

## Perubahan

- FIS-1 menghitung kebutuhan N, P, dan K berdasarkan status hara dan prioritas fase.
- FIS-2 menghitung kebutuhan koreksi pH berupa Kapur Dolomit dan Belerang.
- `membership.py` menyediakan keanggotaan dan status N/P/K/pH yang dipakai bersama pada dashboard.
- `fertilizer.py` memisahkan konversi target hara menjadi dosis Urea, SP-36, KCl, dan NPK.
- Satu baris `rekomendasi` menjadi header hasil perhitungan.
- Beberapa jenis pupuk disimpan pada `rekomendasi_detail`.
- Riwayat lama tetap dibaca dari kolom `jenis_pupuk`, `dosis`, dan `kategori`.
- Rincian perhitungan disimpan pada `fuzzy_trace`; keluaran Z utama juga disimpan pada kolom terpisah.

## Menjalankan migrasi

1. Hentikan backend dan simulator.
2. Buat backup database PostgreSQL.
3. Jalankan `psql -d NAMA_DATABASE -v ON_ERROR_STOP=1 -f backend/migrations/002_fis1_fis2_multi_fertilizer.sql`.
4. Pastikan tabel `rekomendasi_detail` dan kolom baru telah tersedia.
5. Jalankan backend lalu uji `/recommendation/generate`, `/recommendation/latest`, `/recommendation/history`, `/recommendation/export`, `/monitoring/latest`, dan penghapusan rekomendasi.

`backend/main.py` juga menyiapkan kolom dan tabel detail secara idempoten saat startup, mengikuti pola migrasi ringan yang telah digunakan proyek. Skrip SQL tetap disediakan agar perubahan skema dapat diterapkan dan diperiksa secara eksplisit.

## Catatan batasan data

Model monitoring proyek saat ini memiliki `humidity` (kelembapan udara), tetapi belum mempunyai `soil_moisture` (kelembapan tanah). Keduanya tidak boleh dipertukarkan. Karena itu, rekomendasi FIS-1/FIS-2 hanya menggunakan N, P, K, dan pH; catatan kelembapan tanah dari proyek acuan dilewati sampai tersedia kolom kelembapan tanah tersendiri. Kelembapan udara tetap disimpan sebagai konteks monitoring dan tidak dimasukkan ke fungsi kelembapan tanah.

Profil A dan B, D_ref, persentase kandungan pupuk, ambang hujan, serta bentuk fungsi keanggotaan mengikuti ZIP acuan. D_ref dan rentang dosis Dolomit/Belerang pada sumber acuan masih memerlukan verifikasi agronomi. Nilai tersebut tidak boleh ditafsirkan sebagai dosis lapangan tervalidasi sebelum sumber dan satuannya dipastikan.

Dashboard menerima `fuzzy_status` N/P/K/pH dari endpoint monitoring. Riwayat rekomendasi menyediakan parameter `limit`; halaman riwayat meminta 10 baris terbaru, sedangkan analitik dashboard tetap dapat membaca seluruh riwayat.

Data N/P/K dalam aplikasi saat ini disimpan dengan satuan mg/kg. Konversi dari target hara ke dosis pupuk pada ZIP acuan merupakan formula yang dipertahankan sebagai metode rujukan; interpretasi agronomis hasilnya tetap perlu diverifikasi terhadap basis satuan dan takaran aplikasi yang digunakan pada penelitian.
