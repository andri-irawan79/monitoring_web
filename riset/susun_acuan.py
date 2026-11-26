"""Menyusun dan mengunci tabel keputusan acuan v1.0 (subbab 3.8.2b dan 3.8.2d).

Skrip ini SENGAJA tidak mengimpor fuzzy_tsukamoto.py: acuan harus berdiri sendiri dan berupa tabel tegas
(status hara = himpunan dengan derajat keanggotaan tertinggi; kategori = aturan nilai ordinal terkecil).

Keluaran:
  tabel_acuan_v1.json      tabel keputusan lengkap (45 baris hara-fase-status + acuan pH + catatan)
  tabel_acuan_v1.sha256    sidik jari SHA-256 isi JSON; catat di naskah dan commit ke repositori sebelum implementasi
  kasus_uji_acuan.csv      30 baris data simulasi (stratifikasi kelas N, seed 42) x 5 fase x 3 hara = 450 pengamatan
  kasus_uji_acuan_ph.csv   skenario pH dari skenario_uji.csv beserta kategori acuan Dolomit dan Belerang

Pemakaian: python susun_acuan.py   (membutuhkan data_simulasi_365.csv dan skenario_uji.csv di folder yang sama)
"""
import csv, hashlib, json

VERSI = "1.0"
TANGGAL = "2026-11-19"
SEED = 42

HIMPUNAN = {"N": (15, 31, 49), "P": (17, 27, 60), "K": (27, 35, 47)}      # (a, c, b) profil A, subbab 3.6.2
DREF = {"N": 575.0, "P": 245.0, "K": 855.0}                                  # g hara, subbab 3.6.8
PRIORITAS = {                                                                # subbab 3.6.4
    "Pascapanen": {"N": "Sedang", "P": "Sedang", "K": "Sedang"},
    "Vegetatif":  {"N": "Tinggi", "P": "Sedang", "K": "Rendah"},
    "Pembungaan": {"N": "Rendah", "P": "Sedang", "K": "Sedang"},
    "Pembuahan":  {"N": "Sedang", "P": "Sedang", "K": "Tinggi"},
    "Panen":      {"N": "Rendah", "P": "Rendah", "K": "Rendah"},
}
URUT = {"Rendah": 0, "Sedang": 1, "Tinggi": 2}
# kategori kebutuhan acuan: dari kebutuhan menurut status (Rendah->Tinggi, Sedang->Sedang, Tinggi->Tidak perlu)
# dan prioritas fase (Tinggi, Sedang, Rendah), diambil nilai ordinal terkecil
KEBUTUHAN_STATUS = {"Rendah": 2, "Sedang": 1, "Tinggi": 0}
KEBUTUHAN_PRIORITAS = {"Tinggi": 2, "Sedang": 1, "Rendah": 0}
NAMA = {0: "Tidak perlu", 1: "Sedang", 2: "Tinggi"}
RENTANG_PERSEN = {"Tidak perlu": (0, 0), "Sedang": (25, 75), "Tinggi": (75, 100)}     # % D_ref, subbab 3.8.2b


def batas_kelas(abc):
    a, c, b = abc
    return (a + c) / 2, (c + b) / 2          # titik silang himpunan bersebelahan; sama dengan -> kelas lebih rendah

def kelas_hara(x, abc):
    m1, m2 = batas_kelas(abc)
    return "Rendah" if x <= m1 else "Sedang" if x <= m2 else "Tinggi"

def kelas_ph(x):
    return "Masam" if x <= 5.0 else "Normal" if x <= 7.25 else "Basa"   # titik silang 5,0 dan 7,25 (subbab 3.6.2)

def kategori(status, prioritas):
    return NAMA[min(KEBUTUHAN_STATUS[status], KEBUTUHAN_PRIORITAS[prioritas])]

def susun_tabel():
    baris = []
    for fase, per_hara in PRIORITAS.items():
        for hara, p in per_hara.items():
            for status in ("Rendah", "Sedang", "Tinggi"):
                kat = kategori(status, p)
                lo, hi = RENTANG_PERSEN[kat]
                baris.append({"fase": fase, "hara": hara, "prioritas": p, "status": status, "kategori": kat,
                              "persen_dref_min": lo, "persen_dref_maks": hi,
                              "g_hara_min": round(lo / 100 * DREF[hara], 1), "g_hara_maks": round(hi / 100 * DREF[hara], 1)})
    return baris

def acuan_lengkap():
    return {
        "versi": VERSI, "tanggal": TANGGAL,
        "himpunan_abc": HIMPUNAN,
        "batas_kelas": {h: list(batas_kelas(v)) for h, v in HIMPUNAN.items()},
        "dref_g_hara": DREF,
        "kategori_sistem_dari_Z": {"Tidak perlu": "Z < 10", "Sedang": "10 <= Z < 75", "Tinggi": "Z >= 75"},
        "tabel": susun_tabel(),
        "acuan_ph": {"batas": {"Masam": "pH <= 5,0", "Normal": "5,0 < pH <= 7,25", "Basa": "pH > 7,25"},
                     "Masam": {"dolomit": "Diperlukan", "belerang": "Tidak diperlukan"},
                     "Normal": {"dolomit": "Tidak diperlukan", "belerang": "Tidak diperlukan"},
                     "Basa": {"dolomit": "Tidak diperlukan", "belerang": "Diperlukan"},
                     "fase_Panen": "Dolomit dan Belerang tidak ditampilkan"},
        "catatan": ["pH < 5,5 atau pH > 6,5", "status kelembapan Kering atau Basah (derajat tertinggi)",
                    "curah hujan > 200 mm", "seluruh dosis = 0"],
    }

def main():
    import pandas as pd
    acuan = acuan_lengkap()
    isi = json.dumps(acuan, sort_keys=True, ensure_ascii=False, indent=1)
    open("tabel_acuan_v1.json", "w", encoding="utf-8").write(isi)
    sidik = hashlib.sha256(isi.encode("utf-8")).hexdigest()
    open("tabel_acuan_v1.sha256", "w").write(sidik + "  tabel_acuan_v1.json\n")

    d = pd.read_csv("data_simulasi_365.csv")
    d["kelas_N"] = [kelas_hara(x, HIMPUNAN["N"]) for x in d.N]
    sampel = pd.concat([g.sample(n=10, random_state=SEED) for _, g in d.groupby("kelas_N")]).sort_values("hari")
    tab = {(r["fase"], r["hara"], r["status"]): r for r in acuan["tabel"]}
    with open("kasus_uji_acuan.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["hari", "N", "P", "K", "fase", "hara", "nilai", "status", "prioritas", "kategori_acuan", "g_hara_min", "g_hara_maks"])
        for _, r in sampel.iterrows():
            for fase in PRIORITAS:
                for hara in "NPK":
                    st = kelas_hara(r[hara], HIMPUNAN[hara])
                    t = tab[(fase, hara, st)]
                    w.writerow([int(r.hari), r.N, r.P, r.K, fase, hara, r[hara], st, t["prioritas"], t["kategori"], t["g_hara_min"], t["g_hara_maks"]])
    with open("skenario_uji.csv", encoding="utf-8") as f, open("kasus_uji_acuan_ph.csv", "w", newline="", encoding="utf-8") as g:
        w = csv.writer(g); w.writerow(["id", "ph", "kelas_ph", "dolomit_acuan", "belerang_acuan"])
        for r in csv.DictReader(f):
            if r["kelompok"].startswith("C."):
                k = kelas_ph(float(r["ph"]))
                w.writerow([r["id"], r["ph"], k, acuan["acuan_ph"][k]["dolomit"], acuan["acuan_ph"][k]["belerang"]])
    print("SHA-256:", sidik)
    print("kelas N pada 30 baris sampel:", sampel.kelas_N.value_counts().to_dict())
    for h in "PK":
        print(f"kelas {h}:", pd.Series([kelas_hara(x, HIMPUNAN[h]) for x in sampel[h]]).value_counts().to_dict())

if __name__ == "__main__":
    main()
