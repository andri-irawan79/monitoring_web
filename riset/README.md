# riset/ : implementasi acuan, uji, dan tabel acuan terkunci

Folder ini adalah **bukti penelitian**, terpisah dari aplikasi. Jangan mengubah berkas bertanda TERKUNCI.

| Berkas | Fungsi |
|---|---|
| `tabel_acuan_v1.json` / `.sha256` | **TERKUNCI.** Tabel keputusan acuan v1.0 (SHA-256 `3f9e0b81...0eaf`). Dibuat sebelum implementasi dan diuji otomatis; perubahan = versi baru dengan alasan tertulis. |
| `kasus_uji_acuan.csv`, `kasus_uji_acuan_ph.csv` | 450 kombinasi uji hara dan 13 skenario pH beserta kategori acuan |
| `skenario_uji.csv` | 55 skenario uji (51 valid, 4 tidak valid); dapat dijalankan melalui `python backend/simulator/simulator.py --uji` dari root repository |
| `data_simulasi_365.csv` | Data simulasi (6 tanaman buah, seed 42); simulator menghasilkan sampel yang identik |
| `fuzzy_tsukamoto.py` | Implementasi acuan mandiri untuk pembanding hitung manual (`python fuzzy_tsukamoto.py`) |
| `uji_pembanding_crisp.py`, `uji_kewajaran.py` | Skrip uji mandiri (versi otomatis ada di `backend/tests/`) |
| `susun_acuan.py`, `siapkan_data.py` | Pembuat tabel acuan dan data simulasi (tidak mengimpor mesin aplikasi) |
| `baseline_lama.json` | Keluaran **mesin lama** (satu pupuk terpilih, dosis gabungan tanpa satuan) pada 600 baris buah x 5 fase dan 51 skenario. Mesin lama sudah dihapus dari repositori; berkas ini satu-satunya bukti "sebelum" untuk BAB IV. |

Uji otomatis: `cd backend && pytest -q`.


## Menjalankan skenario melalui API PATCH

Dari root repository, jalankan `python backend/simulator/simulator.py --uji`.
Simulator mengautentikasi akun, membuat sesi `scenario` dengan target 51 record,
mengirim 51 kasus valid sebagai data monitoring, dan mengirim 4 kasus tidak valid
tanpa metadata sesi agar ditolak oleh validasi API sebelum penyimpanan. Hasil dianggap
sesuai hanya jika 51 kasus menghasilkan HTTP 200 dan 4 kasus menghasilkan HTTP 422
pada field yang sudah ditentukan. Data sesi skenario tidak ditampilkan pada monitoring
dan riwayat rekomendasi normal. Pengujian ini menilai validasi/penerimaan API, bukan
akurasi rekomendasi fuzzy.


## Revisi fase dan matriks prioritas v1.1

Versi 1.1 mempertahankan ID fase database lama untuk menjaga foreign key, tetapi mengubah label ID 2 menjadi **Prapembungaan** dan ID 4 menjadi **Prapanen**. Label historis disimpan pada kolom `fase_nama_snapshot` agar perubahan master tidak mengubah tampilan rekomendasi lama. Urutan fase pada endpoint diatur sesuai siklus operasional.

Matriks prioritas kualitatif v1.1 berada pada `backend/fuzzy/rules.py` dan `riset/fuzzy_tsukamoto.py`; prioritas fase tidak dinyatakan dalam persentase. D_ref v1.1 dikalibrasi terhadap target tahunan satu studi Monthong Thailand, bukan standar dosis lokal.

Gunakan `python susun_acuan_v1_1.py` dari direktori riset untuk mereproduksi file acuan v1.1. File tabel v1.0 dan checksum-nya tetap dipertahankan.
