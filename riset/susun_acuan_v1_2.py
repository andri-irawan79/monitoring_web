"""Membangun tabel acuan FIS-1 v1.2 dan 450 kasus konsistensi.
Sampel 30 baris dipertahankan dari 450 kasus v1.1; file versi lama tidak ditimpa.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHASES = ["Pascapanen", "Vegetatif", "Prapembungaan", "Pembuahan", "Prapanen"]
PRIORITAS = {
    "Pascapanen": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
    "Vegetatif": {"N": "tinggi", "P": "sedang", "K": "tinggi"},
    "Prapembungaan": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
    "Pembuahan": {"N": "sedang", "P": "sedang", "K": "tinggi"},
    "Prapanen": {"N": "tinggi", "P": "tidak_diperlukan", "K": "tinggi"},
}
RULES = {
    ("rendah", "tinggi"): "tinggi", ("rendah", "sedang"): "sedang",
    ("rendah", "rendah"): "rendah", ("sedang", "tinggi"): "sedang",
    ("sedang", "sedang"): "sedang", ("sedang", "rendah"): "rendah",
    ("tinggi", "tinggi"): "tidak_perlu", ("tinggi", "sedang"): "tidak_perlu",
    ("tinggi", "rendah"): "tidak_perlu",
    ("rendah", "tidak_diperlukan"): "tidak_perlu",
    ("sedang", "tidak_diperlukan"): "tidak_perlu",
    ("tinggi", "tidak_diperlukan"): "tidak_perlu",
}
ABC = {"N": (15, 31, 49), "P": (17, 27, 60), "K": (27, 35, 47)}
DREF = {"N": 1150 / 2.712, "P": 490 / 3, "K": 1710 / 5}
OUTPUT_RANGE = {
    "tidak_perlu": (0, 0), "rendah": (10.6, 20.6),
    "sedang": (0, 50), "tinggi": (50, 100),
}
OUTPUT_NAME = {
    "tidak_perlu": "Tidak perlu", "rendah": "Rendah",
    "sedang": "Sedang", "tinggi": "Tinggi",
}


def status(value, nutrient):
    a, c, b = ABC[nutrient]
    if value <= (a + c) / 2:
        return "rendah"
    if value <= (c + b) / 2:
        return "sedang"
    return "tinggi"


def main():
    table = []
    for phase in PHASES:
        for nutrient in ("N", "P", "K"):
            for status_name in ("rendah", "sedang", "tinggi"):
                consequent = RULES[(status_name, PRIORITAS[phase][nutrient])]
                low, high = OUTPUT_RANGE[consequent]
                table.append({
                    "fase": phase, "hara": nutrient,
                    "prioritas": PRIORITAS[phase][nutrient],
                    "status": status_name.capitalize(),
                    "kategori": OUTPUT_NAME[consequent],
                    "persen_dref_min": low, "persen_dref_maks": high,
                })

    acuan = {
        "versi": "1.2",
        "tanggal": "2026-11-27",
        "fase": PHASES,
        "matriks_prioritas": PRIORITAS,
        "himpunan_abc": ABC,
        "dref_g_hara": DREF,
        "fungsi_keluaran_fis1": {
            "Tidak perlu": "z = 0",
            "Rendah": "z = 20,6 - 10 alpha; rentang 10,6-20,6",
            "Sedang": "z = 50 alpha; rentang 0-50",
            "Tinggi": "z = 50 + 50 alpha; rentang 50-100",
        },
        "aturan_fis1": {f"{s}|{p}": r for (s, p), r in RULES.items()},
        "sumber_basis": "Direktorat Buah dan Florikultura (2021), Buku Lapang Budidaya Durian, Tabel 7; sumber angka pada tabel: Haifa Thailand.",
        "tabel": table,
        "catatan": [
            "Prioritas Rendah tidak identik dengan Tidak perlu; kebutuhan Rendah tetap memiliki keluaran positif.",
            "Status hara Tinggi menghasilkan Tidak perlu untuk N, P, dan K.",
            "Prioritas P2O5 pada Prapanen dinyatakan Tidak diperlukan mengikuti nilai P2O5 nol pada satu bulan sebelum panen di Tabel 7.",
            "D_ref adalah kalibrasi terhadap satu target tahunan Monthong Thailand, bukan dosis per fase tervalidasi untuk kebun lokal.",
            "FIS-2 tidak berubah dari v1.1.",
            "450 kasus adalah kombinasi 30 baris x 5 fase x 3 hara dan bukan 450 sampel independen.",
        ],
    }
    raw = json.dumps(acuan, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
    (ROOT / "tabel_acuan_v1_2.json").write_text(raw, encoding="utf-8")
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    (ROOT / "tabel_acuan_v1_2.sha256").write_text(
        f"{digest}  tabel_acuan_v1_2.json\n", encoding="utf-8"
    )

    # Pertahankan 30 tanggal unik pertama dari versi 1.1.
    sampled = {}
    with (ROOT / "kasus_uji_acuan_v1_1.csv").open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            sampled.setdefault(row["hari"], {k: float(row[k]) for k in ("N", "P", "K")}
                               | {"hari": row["hari"]})
    with (ROOT / "kasus_uji_acuan_v1_2.csv").open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["hari", "N", "P", "K", "fase", "hara", "nilai", "status",
                         "prioritas", "kategori_acuan", "g_hara_min", "g_hara_maks"])
        for base in list(sampled.values())[:30]:
            for phase in PHASES:
                for nutrient in ("N", "P", "K"):
                    st = status(base[nutrient], nutrient)
                    consequent = RULES[(st, PRIORITAS[phase][nutrient])]
                    low, high = OUTPUT_RANGE[consequent]
                    writer.writerow([
                        base["hari"], base["N"], base["P"], base["K"],
                        phase, nutrient, base[nutrient], st.capitalize(),
                        PRIORITAS[phase][nutrient], OUTPUT_NAME[consequent],
                        f"{low / 100 * DREF[nutrient]:.2f}",
                        f"{high / 100 * DREF[nutrient]:.2f}",
                    ])
    (ROOT / "kasus_uji_acuan_ph_v1_2.csv").write_bytes(
        (ROOT / "kasus_uji_acuan_ph_v1_1.csv").read_bytes()
    )
    print("Tabel acuan FIS-1 v1.2:", digest, "| 450 kombinasi uji")


if __name__ == "__main__":
    main()
