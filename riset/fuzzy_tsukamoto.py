"""Implementasi acuan fuzzy Tsukamoto untuk rekomendasi pemupukan durian Monthong.

Mengikuti BAB III: himpunan masukan (3.6.2), keluaran Tsukamoto (3.6.3), aturan FIS-1 (3.6.4),
catatan (3.6.5), FIS-2 (3.6.6), D_ref (3.6.8), dan Algoritma 4-5 (3.6.11).
Dipakai sebagai pembanding hitung manual dan sebagai dasar uji (uji_pembanding_crisp.py, uji_kewajaran.py).

Cek mandiri contoh perhitungan Lampiran 5:  python fuzzy_tsukamoto.py
"""
import math

FASE = ["Pascapanen", "Vegetatif", "Prapembungaan", "Pembuahan", "Prapanen"]

# ---------- parameter (subbab 3.6.2, profil A = kuartil data buah) ----------
# (a, c, b): bahu turun 1 pada <= a dan 0 pada >= c; segitiga (a, c, b); bahu naik 0 pada <= c dan 1 pada >= b
PROFIL_A = {"N": (15, 31, 49), "P": (17, 27, 60), "K": (27, 35, 47)}
# Profil B: batas kelas pedoman uji tanah (3.3.4): a = batas Rendah, b = batas Tinggi, c = titik tengah
PROFIL_B = {"N": (10, 15, 20), "P": (10, 15.5, 21), "K": (50, 87.5, 125)}
KELEMBAPAN = (15, 20, 25)          # Kering / Optimal / Basah

# prioritas fase (subbab 3.6.4)
PRIORITAS = {
    "Pascapanen": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
    "Vegetatif": {"N": "tinggi", "P": "sedang", "K": "tinggi"},
    "Prapembungaan": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
    "Pembuahan": {"N": "sedang", "P": "sedang", "K": "tinggi"},
    "Prapanen": {"N": "tinggi", "P": "rendah", "K": "tinggi"},
}
# aturan FIS-1: (status hara, prioritas fase) -> kebutuhan (R1-R9)
ATURAN1 = {
    ("rendah", "tinggi"): "tinggi", ("rendah", "sedang"): "sedang", ("rendah", "rendah"): "rendah",
    ("sedang", "tinggi"): "sedang", ("sedang", "sedang"): "sedang", ("sedang", "rendah"): "rendah",
    ("tinggi", "tinggi"): "rendah", ("tinggi", "sedang"): "rendah", ("tinggi", "rendah"): "rendah",
}
# aturan FIS-2: pH -> (kebutuhan Dolomit, kebutuhan Belerang)  (K1-K3)
ATURAN2 = {"masam": ("tinggi", "rendah"), "normal": ("rendah", "rendah"), "basa": ("rendah", "tinggi")}

# D_ref (g hara per aplikasi acuan, subbab 3.6.8) dan kandungan pupuk
DREF = {"N": 460.0, "P": 163.33333333333334, "K": 342.0}
KANDUNGAN = {"urea": 0.46, "sp36": 0.36, "kcl": 0.60, "npk": 0.16}
DOLOMIT = (1000, 3000)     # g/pohon, indikatif (tabel 3.6.6, masih placeholder)
BELERANG = (350, 700)      # g/pohon, indikatif
AMBANG_Z = 10.0            # Z di bawah ini dianggap 0
KELIPATAN, DOSIS_MIN = 5, 20
AMBANG_HUJAN = 200.0
# Cara menggabungkan aturan berkonsekuen sama:
#   "jumlah"     = alpha aturan berkonsekuen sama dijumlahkan (maks 1) sebelum dihitung (subbab 3.6.7, Algoritma 4)
#   "per_aturan" = tiap aturan dihitung sendiri (Tsukamoto asli); dipertahankan hanya untuk pembanding
AGREGASI = "jumlah"       # sesuai subbab 3.6.7 (setelah perbaikan); "per_aturan" hanya untuk pembanding


# ---------- fungsi keanggotaan ----------
def turun(x, a, b):
    return 1.0 if x <= a else 0.0 if x >= b else (b - x) / (b - a)

def naik(x, a, b):
    return 0.0 if x <= a else 1.0 if x >= b else (x - a) / (b - a)

def segitiga(x, a, c, b):
    if x <= a or x >= b:
        return 0.0
    return (x - a) / (c - a) if x <= c else (b - x) / (b - c)

def trapesium(x, a, b, c, d):
    if x <= a or x >= d:
        return 0.0
    if x < b:
        return (x - a) / (b - a)
    if x <= c:
        return 1.0
    return (d - x) / (d - c)

def status_hara(x, abc):
    a, c, b = abc
    return {"rendah": turun(x, a, c), "sedang": segitiga(x, a, c, b), "tinggi": naik(x, c, b)}

def status_lembap(x):
    a, c, b = KELEMBAPAN
    return {"kering": turun(x, a, c), "optimal": segitiga(x, a, c, b), "basah": naik(x, c, b)}

def status_ph(x):
    return {"masam": turun(x, 4.5, 5.5), "normal": trapesium(x, 4.5, 5.5, 6.5, 8.0), "basa": naik(x, 6.5, 8.0)}


# ---------- Tsukamoto (Algoritma 4) ----------
def z_keluaran(kelas, alpha):
    if kelas == "rendah":
        return 10 * (1 - alpha)
    if kelas == "sedang":
        return 50 * alpha
    return 50 + 50 * alpha            # tinggi

def tsukamoto(aturan_aktif):
    """aturan_aktif: daftar (alpha, kelas_keluaran). Mengembalikan Z (0-100), di bawah ambang dianggap 0."""
    if AGREGASI == "jumlah":
        gabung = {}
        for alpha, kelas in aturan_aktif:
            gabung[kelas] = min(1.0, gabung.get(kelas, 0.0) + alpha)
        aturan_aktif = [(a, k) for k, a in gabung.items()]
    pembilang = penyebut = 0.0
    for alpha, kelas in aturan_aktif:
        if alpha > 0:
            pembilang += alpha * z_keluaran(kelas, alpha)
            penyebut += alpha
    z = pembilang / penyebut if penyebut > 0 else 0.0
    return 0.0 if z < AMBANG_Z else z

def z_fis1(nilai, hara, fase, profil=PROFIL_A):
    mu = status_hara(nilai, profil[hara])
    p = PRIORITAS[fase][hara]
    return tsukamoto([(mu[s], ATURAN1[(s, p)]) for s in mu])

def z_fis2(ph):
    mu = status_ph(ph)
    dol = tsukamoto([(mu[s], ATURAN2[s][0]) for s in mu])
    bel = tsukamoto([(mu[s], ATURAN2[s][1]) for s in mu])
    return dol, bel


# ---------- rekomendasi (Algoritma 5) ----------
def bulat(x):
    nilai = int(math.floor(x / KELIPATAN + 0.5) * KELIPATAN)
    return 0 if nilai < DOSIS_MIN else nilai

def rekomendasi(N, P, K, ph, lembap, hujan, fase, profil=PROFIL_A, dref=DREF):
    z = {h: z_fis1(v, h, fase, profil) for h, v in (("N", N), ("P", P), ("K", K))}
    z_dol, z_bel = z_fis2(ph)
    t = {h: z[h] / 100 * dref[h] for h in z}                       # target hara (g)
    npk = min(t.values()) / KANDUNGAN["npk"] if all(z[h] > 0 for h in z) else 0.0
    sisa = {h: max(0.0, t[h] - KANDUNGAN["npk"] * npk) for h in t}
    dosis = {
        "urea": bulat(sisa["N"] / KANDUNGAN["urea"]),
        "sp36": bulat(sisa["P"] / KANDUNGAN["sp36"]),
        "kcl": bulat(sisa["K"] / KANDUNGAN["kcl"]),
        "npk": bulat(npk),
    }
    # FIS-2 hanya bergantung pada pH, sehingga dihitung pada seluruh fase.
    koreksi = {"dolomit": tuple(round(z_dol / 100 * v) for v in DOLOMIT),
               "belerang": tuple(round(z_bel / 100 * v) for v in BELERANG)}
    catatan = []
    if ph < 5.5 or ph > 6.5:
        catatan.append("pH di luar kisaran optimal; koreksi pH lebih dahulu")
    mu = status_lembap(lembap)
    s = max(mu, key=mu.get)
    if s == "kering":
        catatan.append("pastikan tanah cukup lembap")
    if s == "basah":
        catatan.append("tunda atau pecahkan dosis")
    if hujan > AMBANG_HUJAN:
        catatan.append("pecahkan dosis (curah hujan tinggi)")
    if not any(dosis.values()):
        catatan.append("pemupukan tidak dianjurkan pada kondisi atau fase ini")
    return {"Z": z, "Z_dolomit": z_dol, "Z_belerang": z_bel, "target": t, "dosis": dosis,
            "koreksi": koreksi, "catatan": catatan}

def hara_dari_dosis(d):
    """Dosis pupuk (g) -> gram hara N, P2O5, K2O."""
    k = KANDUNGAN
    return {"N": d["urea"] * k["urea"] + d["npk"] * k["npk"],
            "P": d["sp36"] * k["sp36"] + d["npk"] * k["npk"],
            "K": d["kcl"] * k["kcl"] + d["npk"] * k["npk"]}


def _cek_mandiri():
    """Contoh 1 dan 2 pada Lampiran 5 (hitung manual) harus sama dengan keluaran program."""
    r1 = rekomendasi(40, 45, 30, 6.0, 20, 100, "Vegetatif")["dosis"]
    r2 = rekomendasi(10, 10, 15, 6.0, 20, 100, "Pascapanen")["dosis"]
    r3 = rekomendasi(10, 10, 15, 6.0, 20, 100, "Prapanen")["dosis"]
    assert r1 == {"urea": 105, "sp36": 0, "kcl": 295, "npk": 130}, r1
    assert r2 == {"urea": 0, "sp36": 455, "kcl": 570, "npk": 0}, r2
    assert r3 == {"urea": 1000, "sp36": 0, "kcl": 570, "npk": 0}, r3
    print("Cek mandiri v1.1 lolos:", r1, r2, r3)

if __name__ == "__main__":
    _cek_mandiri()
