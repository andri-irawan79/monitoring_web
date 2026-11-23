"""Tabel acuan v1.0 (riset/) harus tidak berubah, dan mesin aplikasi harus sesuai acuan pada ambang yang ditetapkan
sebelum pengujian (subbab 3.9): akurasi kategori >= 90% dan dosis dalam kisaran >= 90%; pH dilaporkan terpisah."""
import csv
import hashlib
from pathlib import Path

from fuzzy.tsukamoto import hitung_rekomendasi

RISET = Path(__file__).resolve().parent.parent.parent / "riset"
SHA_TERKUNCI = "3f9e0b81a57f3f17ca2acd7ee9e0972669fd05b28c6ec899ed1f6612d6420eaf"


def _csv(nama):
    with open(RISET / nama, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _kategori(z):
    return "Tidak perlu" if z < 10 else "Sedang" if z < 75 else "Tinggi"


def test_tabel_acuan_tidak_berubah():
    tercatat = (RISET / "tabel_acuan_v1.sha256").read_text().split()[0]
    nyata = hashlib.sha256((RISET / "tabel_acuan_v1.json").read_bytes()).hexdigest()
    assert tercatat == SHA_TERKUNCI, "berkas .sha256 diubah"
    assert nyata == SHA_TERKUNCI, "tabel_acuan_v1.json diubah; buat versi baru, jangan menimpa v1.0"


def test_kesesuaian_450_pengamatan_hara():
    rentang = {"Tidak perlu": (0.0, 0.0), "Sedang": (25.0, 75.0), "Tinggi": (75.0, 100.0)}
    kasus = _csv("kasus_uji_acuan.csv")
    assert len(kasus) == 450
    sama = dalam = 0
    for r in kasus:
        nilai = {"N": 40.0, "P": 27.0, "K": 35.0}                  # hara lain pada nilai tetap; hanya satu hara yang diuji
        nilai[r["hara"]] = float(r["nilai"])
        z = hitung_rekomendasi(nilai["N"], nilai["P"], nilai["K"], 6.0, 100, r["fase"], kelembapan_tanah=20)["z"][r["hara"].lower()]
        sama += _kategori(z) == r["kategori_acuan"]
        lo, hi = rentang[r["kategori_acuan"]]
        dalam += (z == 0) if r["kategori_acuan"] == "Tidak perlu" else (lo - 1e-9 <= z <= hi + 1e-9)
    assert sama / 450 >= 0.90, f"akurasi kategori {sama}/450"
    assert dalam / 450 >= 0.90, f"dosis dalam kisaran {dalam}/450"


def test_acuan_ph_dilaporkan_terpisah():
    kasus = _csv("kasus_uji_acuan_ph.csv")
    cocok = 0
    for r in kasus:
        k = hitung_rekomendasi(31, 27, 35, float(r["ph"]), 100, "Vegetatif", kelembapan_tanah=20)["z"]
        dol = "Diperlukan" if k["dolomit"] > 0 else "Tidak diperlukan"
        bel = "Diperlukan" if k["belerang"] > 0 else "Tidak diperlukan"
        cocok += dol == r["dolomit_acuan"] and bel == r["belerang_acuan"]
    # Selisih diharapkan hanya di zona transisi (pH 5,0-5,5 dan 6,5-7,25); batas bawah wajar 75%.
    assert len(kasus) == 13 and cocok / 13 >= 0.75, f"pH cocok {cocok}/13"
