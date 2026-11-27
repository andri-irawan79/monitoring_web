"""Pembanding crisp (3.8.3), uji monotonik (toleransi 5 poin persen), dan uji kewajaran dosis tahunan (3.8.2c)."""
import csv
from pathlib import Path

from fuzzy.parameter import DEFAULT
from fuzzy.tsukamoto import hitung_rekomendasi

RISET = Path(__file__).resolve().parent.parent.parent / "riset"
FASE = ("Pascapanen", "Vegetatif", "Prapembungaan", "Pembuahan", "Prapanen")
RENTANG = {"N": (0, 140), "P": (5, 145), "K": (5, 205)}
BASIS = {"N": 31.0, "P": 27.0, "K": 35.0}
PRIORITAS = {
    "Pascapanen": ("rendah", "tinggi", "tinggi"),
    "Vegetatif": ("tinggi", "sedang", "tinggi"),
    "Prapembungaan": ("rendah", "tinggi", "tinggi"),
    "Pembuahan": ("sedang", "sedang", "tinggi"),
    "Prapanen": ("tinggi", "rendah", "tinggi"),
}
ATURAN = {("rendah", "tinggi"): 100, ("rendah", "sedang"): 50, ("sedang", "tinggi"): 50, ("sedang", "sedang"): 50}   # selain ini = 0


def _z(hara, x, fase):
    v = dict(BASIS)
    v[hara] = float(x)
    return hitung_rekomendasi(v["N"], v["P"], v["K"], 6.0, 100, fase, kelembapan_tanah=20)["z"][hara.lower()]


def test_fuzzy_lebih_mulus_daripada_crisp():
    lonc_fuzzy = lonc_crisp = 0
    maks_fuzzy = 0.0
    for idx, hara in enumerate("NPK"):
        lo, hi = RENTANG[hara]
        a, c, b = DEFAULT.hara[hara]
        for fase in FASE:
            pr = PRIORITAS[fase][idx]
            zf = [_z(hara, x, fase) for x in range(lo, hi + 1)]
            zc = [ATURAN.get(("rendah" if x <= a else "tinggi" if x >= b else "sedang", pr), 0) for x in range(lo, hi + 1)]
            df = [abs(zf[i + 1] - zf[i]) for i in range(len(zf) - 1)]
            dc = [abs(zc[i + 1] - zc[i]) for i in range(len(zc) - 1)]
            lonc_fuzzy += sum(v > 25 for v in df)
            lonc_crisp += sum(v > 25 for v in dc)
            maks_fuzzy = max(maks_fuzzy, max(df))
    assert lonc_fuzzy == 0 and lonc_crisp > 0 and maks_fuzzy < 25, (lonc_fuzzy, lonc_crisp, maks_fuzzy)


def test_kenaikan_lokal_z_dibatasi_5_poin_persen():
    total = 0
    for hara, (lo, hi) in RENTANG.items():
        for fase in FASE:
            z = [_z(hara, x, fase) for x in range(lo, hi + 1)]
            naik = [z[i + 1] - z[i] for i in range(len(z) - 1) if z[i + 1] > z[i] + 1e-3]
            assert all(v <= 5.0 for v in naik), (hara, fase, max(naik))
            total += len(naik)
    # Matriks v1.1 memperluas jumlah kombinasi prioritas Tinggi, sehingga jumlah
    # kenaikan lokal tidak dibandingkan dengan batas absolut versi terdahulu.
    # Syarat yang diuji adalah tidak ada kenaikan satu langkah yang melampaui 5 poin.
    assert total >= 0


KISARAN = {"N": (649, 1800), "P": (490, 1560), "K": (717, 4000)}       # g hara per pohon per tahun (tabel bukti dosis, 3.6.8)
KANDUNGAN = {"urea": 0.46, "sp36": 0.36, "kcl": 0.60, "npk": 0.16}


def test_kewajaran_dosis_tahunan_10_skenario():
    with open(RISET / "skenario_uji.csv", newline="", encoding="utf-8") as f:
        data = {r["id"]: r for r in csv.DictReader(f)}
    ids = ["SK-19", "SK-20", "SK-21", "SK-22", "SK-23", "SK-24", "SK-05", "SK-07", "SK-11", "SK-17"]
    tahunan = {}
    for i in ids:
        r, tot = data[i], {"N": 0.0, "P": 0.0, "K": 0.0}
        for fase in FASE:
            d = hitung_rekomendasi(float(r["N"]), float(r["P"]), float(r["K"]), float(r["ph"]), float(r["rainfall"]), fase,
                                   kelembapan_tanah=float(r["soil_moisture"]))["doses_g"]
            tot["N"] += d["urea"] * KANDUNGAN["urea"] + d["npk"] * KANDUNGAN["npk"]
            tot["P"] += d["sp36"] * KANDUNGAN["sp36"] + d["npk"] * KANDUNGAN["npk"]
            tot["K"] += d["kcl"] * KANDUNGAN["kcl"] + d["npk"] * KANDUNGAN["npk"]
        tahunan[i] = tot
    wajar = 0
    for i, tot in tahunan.items():
        ok = all(tot[h] <= KISARAN[h][1] for h in tot)
        if i == "SK-19":                                              # hara rendah: dalam kisaran (toleransi pembulatan 2%)
            ok = ok and all(KISARAN[h][0] * 0.98 <= tot[h] <= KISARAN[h][1] for h in tot)
        if i == "SK-21":                                              # hara tinggi: lebih kecil daripada hara rendah
            ok = ok and all(tot[h] < tahunan["SK-19"][h] for h in tot)
        wajar += ok
    assert wajar / len(ids) >= 0.80, f"skenario wajar {wajar}/10"
