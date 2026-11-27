"""Build versi 1.1; data sampel 30 hari pertama memakai basis kasus terkunci v1.0."""
import csv, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHASES = ["Pascapanen", "Vegetatif", "Prapembungaan", "Pembuahan", "Prapanen"]
PRIORITAS = {
    "Pascapanen": {"N": "Rendah", "P": "Tinggi", "K": "Tinggi"},
    "Vegetatif": {"N": "Tinggi", "P": "Sedang", "K": "Tinggi"},
    "Prapembungaan": {"N": "Rendah", "P": "Tinggi", "K": "Tinggi"},
    "Pembuahan": {"N": "Sedang", "P": "Sedang", "K": "Tinggi"},
    "Prapanen": {"N": "Tinggi", "P": "Rendah", "K": "Tinggi"},
}
ABC = {"N": (15, 31, 49), "P": (17, 27, 60), "K": (27, 35, 47)}
DREF = {"N": 460, "P": 490 / 3, "K": 342}
RANK = {"Rendah": 0, "Sedang": 1, "Tinggi": 2}
RANGE = {"Tidak perlu": (0, 0), "Sedang": (10, 75), "Tinggi": (75, 100)}
DEFINISI = {
    "Pascapanen": "Setelah buah terakhir dipetik sampai muncul flush baru.",
    "Vegetatif": "Flush atau tunas baru pada pohon produktif sampai daun matang.",
    "Prapembungaan": "Setelah flush matang sampai sebelum bunga pertama mekar; acuan literatur 1–2 bulan sebelum berbunga.",
    "Pembuahan": "Kategori generatif operasional: bunga mekar, pembentukan pentil, dan pembesaran buah sampai jendela prapanen.",
    "Prapanen": "Kira-kira satu bulan sebelum perkiraan panen sampai pemetikan pertama; panen aktif tidak dimodelkan tersendiri.",
}
BASIS = {
    "Pascapanen": "Satu minggu setelah panen: N 45–90, P2O5 135–270, K2O 135–270 g/tanaman.",
    "Vegetatif": "Saat keluar pucuk daun: N 210–420, P2O5 105–210, K2O 420–840 g/tanaman.",
    "Prapembungaan": "Satu sampai dua bulan sebelum berbunga: N 45–90, P2O5 135–270, K2O 135–270 g/tanaman.",
    "Pembuahan": "Menggabungkan bunga mekar, pentil buah, dan pembesaran buah; prioritas agregat N sedang, P sedang, K tinggi.",
    "Prapanen": "Satu bulan sebelum panen: N 260–390, P2O5 0, K2O 920–1400 g/tanaman.",
}


def status(value, hara):
    a, c, b = ABC[hara]
    if value <= (a + c) / 2:
        return "Rendah"
    if value <= (c + b) / 2:
        return "Sedang"
    return "Tinggi"


def category(st, pr):
    # Konsekuen sama persis dengan sembilan rule FIS-1.
    if st == "Tinggi":
        return "Tidak perlu"
    if st == "Rendah":
        return {"Rendah": "Tidak perlu", "Sedang": "Sedang", "Tinggi": "Tinggi"}[pr]
    return {"Rendah": "Tidak perlu", "Sedang": "Sedang", "Tinggi": "Sedang"}[pr]


def main():
    table = []
    for phase in PHASES:
        for hara in ("N", "P", "K"):
            for st in ("Rendah", "Sedang", "Tinggi"):
                cat = category(st, PRIORITAS[phase][hara])
                low, high = RANGE[cat]
                table.append({"fase": phase, "hara": hara, "prioritas": PRIORITAS[phase][hara],
                              "status": st, "kategori": cat,
                              "persen_dref_min": low, "persen_dref_maks": high})
    acuan = {
        "versi": "1.1", "tanggal": "2026-11-27", "fase": PHASES,
        "definisi_fase": DEFINISI, "basis_prioritas": BASIS,
        "sumber_basis": "Direktorat Buah dan Florikultura (2021), Buku Lapang Budidaya Durian, Tabel 7; sumber tabel: Haifa Thailand.",
        "himpunan_abc": ABC, "batas_kelas": {"N": [23, 40], "P": [22, 43.5], "K": [31, 41]},
        "dref_g_hara": DREF,
        "kategori_sistem_dari_Z": {"Tidak perlu": "Z < 10", "Sedang": "10 <= Z < 75", "Tinggi": "Z >= 75"},
        "tabel": table,
        "acuan_ph": {
            "batas": {"Masam": "pH <= 5,0", "Normal": "5,0 < pH <= 7,25", "Basa": "pH > 7,25"},
            "Masam": {"dolomit": "Diperlukan", "belerang": "Tidak diperlukan"},
            "Normal": {"dolomit": "Tidak diperlukan", "belerang": "Tidak diperlukan"},
            "Basa": {"dolomit": "Tidak diperlukan", "belerang": "Diperlukan"},
            "cakupan_fase": "FIS-2 dihitung pada seluruh fase; koreksi tetap indikatif dan perlu diverifikasi dengan analisis tanah.",
        },
        "catatan": [
            "Prioritas Rendah/Sedang/Tinggi adalah pemetaan ordinal kualitatif, bukan persentase dosis tahunan per fase.",
            "Pembuahan menggabungkan beberapa stadia generatif yang memiliki variasi kebutuhan hara.",
            "Data penelitian berupa simulasi dan bukan hasil analisis tanah kebun durian Monthong.",
            "D_ref merupakan kalibrasi matematis terhadap target tahunan satu studi Monthong Thailand, bukan dosis lapangan tervalidasi.",
            "Keluaran Dolomit dan Belerang indikatif dan memerlukan analisis tanah atau kebutuhan kapur.",
        ],
    }
    raw = json.dumps(acuan, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
    (ROOT / "tabel_acuan_v1_1.json").write_text(raw, encoding="utf-8")
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    (ROOT / "tabel_acuan_v1_1.sha256").write_text(f"{digest}  tabel_acuan_v1_1.json\n", encoding="utf-8")

    sampled = {}
    with (ROOT / "kasus_uji_acuan.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["hari"] not in sampled:
                vals = {h: float(row[h]) for h in ("N", "P", "K")}
                sampled[row["hari"]] = {"hari": row["hari"], **{
                    h: int(v) if v.is_integer() else v for h, v in vals.items()
                }}
    with (ROOT / "kasus_uji_acuan_v1_1.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["hari", "N", "P", "K", "fase", "hara", "nilai", "status", "prioritas", "kategori_acuan", "g_hara_min", "g_hara_maks"])
        for base in list(sampled.values())[:30]:
            for phase in PHASES:
                for hara in ("N", "P", "K"):
                    st = status(base[hara], hara)
                    pr = PRIORITAS[phase][hara]
                    cat = category(st, pr)
                    low, high = RANGE[cat]
                    w.writerow([base["hari"], base["N"], base["P"], base["K"], phase, hara,
                                base[hara], st, pr, cat, f"{low / 100 * DREF[hara]:.1f}",
                                f"{high / 100 * DREF[hara]:.1f}"])
    (ROOT / "kasus_uji_acuan_ph_v1_1.csv").write_bytes((ROOT / "kasus_uji_acuan_ph.csv").read_bytes())
    print("Generated v1.1 reference table and 450 test cases:", digest)


if __name__ == "__main__":
    main()
