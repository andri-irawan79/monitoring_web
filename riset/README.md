# riset/ : implementasi acuan, uji, dan tabel acuan terkunci

Folder ini adalah **bukti penelitian**, terpisah dari aplikasi. Jangan mengubah berkas bertanda TERKUNCI.

| Berkas | Fungsi |
|---|---|
| `tabel_acuan_v1.json` / `.sha256` | **TERKUNCI.** Tabel keputusan acuan v1.0 (SHA-256 `3f9e0b81...0eaf`). Dibuat sebelum implementasi dan diuji otomatis; perubahan = versi baru dengan alasan tertulis. |
| `kasus_uji_acuan.csv`, `kasus_uji_acuan_ph.csv` | 450 pengamatan hara dan 13 skenario pH beserta kategori acuan |
| `skenario_uji.csv` | 55 skenario uji (51 valid, 4 tidak valid) |
| `data_simulasi_365.csv` | Data simulasi (6 tanaman buah, seed 42); simulator menghasilkan sampel yang identik |
| `fuzzy_tsukamoto.py` | Implementasi acuan mandiri untuk pembanding hitung manual (`python fuzzy_tsukamoto.py`) |
| `uji_pembanding_crisp.py`, `uji_kewajaran.py` | Skrip uji mandiri (versi otomatis ada di `backend/tests/`) |
| `susun_acuan.py`, `siapkan_data.py` | Pembuat tabel acuan dan data simulasi (tidak mengimpor mesin aplikasi) |
| `baseline_lama.json` | Keluaran **mesin lama** (satu pupuk terpilih, dosis gabungan tanpa satuan) pada 600 baris buah x 5 fase dan 51 skenario. Mesin lama sudah dihapus dari repositori; berkas ini satu-satunya bukti "sebelum" untuk BAB IV. |

Uji otomatis: `cd backend && pytest -q`.
