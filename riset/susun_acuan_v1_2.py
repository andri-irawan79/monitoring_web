"""Membangun ulang tabel acuan dan 450 kasus konsistensi FIS-1 v1.2."""
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
    ("rendah", "tinggi"): "tinggi",
    ("rendah", "sedang"): "sedang",
    ("rendah", "rendah"): "rendah",
    ("sedang", "tinggi"): "sedang",
    ("sedang", "sedang"): "sedang",
    ("sedang", "rendah"): "rendah",
    ("tinggi", "tinggi"): "tidak_perlu",
    ("tinggi", "sedang"): "tidak_perlu",
    ("tinggi", "rendah"): "tidak_perlu",
    ("rendah", "tidak_diperlukan"): "tidak_perlu",
    ("sedang", "tidak_diperlukan"): "tidak_perlu",
    ("tinggi", "tidak_diperlukan"): "tidak_perlu",
}
ABC = {"N": (15, 31, 49), "P": (17, 27, 60), "K": (27, 35, 47)}
DREF = {"N": 1150 / 2.712, "P": 490 / 3, "K": 342}
OUTPUT_RANGE = {
    "tidak_perlu": (0, 0),
    "rendah": (10.6, 20.6),
    "sedang": (0, 50),
    "tinggi": (50, 100),
}
OUTPUT_NAME = {
    "tidak_perlu": "Tidak perlu",
    "rendah": "Rendah",
    "sedang": "Sedang",
    "tinggi": "Tinggi",
}
DEFINISI_FASE = {
    "Pascapanen": "Setelah buah terakhir dipetik sampai muncul flush baru.",
    "Vegetatif": "Flush atau tunas baru pada pohon produktif sampai daun matang.",
    "Prapembungaan": "Setelah flush matang sampai sebelum bunga pertama mekar; acuan literatur 1–2 bulan sebelum berbunga.",
    "Pembuahan": "Kategori generatif operasional: bunga mekar, pembentukan pentil, dan pembesaran buah sampai jendela prapanen.",
    "Prapanen": "Kira-kira satu bulan sebelum perkiraan panen sampai pemetikan pertama; panen aktif tidak dimodelkan tersendiri.",
}
PH_ACUAN = {
    "batas": {"Masam": "pH <= 5,0", "Normal": "5,0 < pH <= 7,25", "Basa": "pH > 7,25"},
    "Masam": {"dolomit": "Diperlukan", "belerang": "Tidak diperlukan"},
    "Normal": {"dolomit": "Tidak diperlukan", "belerang": "Tidak diperlukan"},
    "Basa": {"dolomit": "Tidak diperlukan", "belerang": "Diperlukan"},
    "cakupan_fase": "FIS-2 tetap seperti v1.1, dihitung pada seluruh fase dan hanya bergantung pada pH.",
}


def get_status(value, hara):
    a, c, b = ABC[hara]
    if value <= (a + c) / 2:
        return "Rendah"
    if value <= (c + b) / 2:
        return "Sedang"
    return "Tinggi"


def build():
    table = []
    for phase in PHASES:
        for hara in ("N", "P", "K"):
            for status in ("Rendah", "Sedang", "Tinggi"):
                consequent = RULES[(status.lower(), PRIORITAS[phase][hara])]
                low, high = OUTPUT_RANGE[consequent]
                table.append({
                    "fase": phase, "hara": hara, "prioritas": PRIORITAS[phase][hara],
                    "status": status, "kategori": OUTPUT_NAME[consequent],
                    "persen_dref_min": low, "persen_dref_maks": high,
                })

    z_values = {
        "N": [10.6, 100, 10.6, 50, 100],
        "P": [100, 50, 100, 50, 0],
        "K": [100, 100, 100, 100, 100],
    }
    acuan = {
        "versi": "1.2",
        "tanggal": "2026-11-27",
        "perubahan_utama": [
            "Konsekuen Tidak perlu dipisahkan dari Rendah pada FIS-1.",
            "Prioritas Rendah menghasilkan kebutuhan kecil nonnol untuk status hara Rendah/Sedang; status hara Tinggi tetap Tidak perlu.",
            "P2O5 pada Prapanen ditetapkan Tidak diperlukan sebagai pengecualian operasional berbasis nilai 0 pada Tabel 7 satu bulan sebelum panen.",
            "FIS-2 tetap memakai fungsi keluaran dan ambang v1.1.",
        ],
        "fase": PHASES,
        "definisi_fase": DEFINISI_FASE,
        "matriks_prioritas": PRIORITAS,
        "sumber_basis": "Direktorat Buah dan Florikultura (2021), Buku Lapang Budidaya Durian, Tabel 7; sumber tabel: Haifa Thailand.",
        "himpunan_abc": ABC,
        "batas_kelas": {"N": [23, 40], "P": [22, 43.5], "K": [31, 41]},
        "dref_g_hara": DREF,
        "fungsi_keluaran_fis1": {
            "TidakPerlu": "Z = 0 untuk semua alpha aktif; konsekuen monoton non-increasing berbentuk langkah.",
            "Rendah": "z = 20,6 - 10 alpha; rentang invers 10,6-20,6% D_ref.",
            "Sedang": "z = 50 alpha; rentang invers 0-50% D_ref.",
            "Tinggi": "z = 50 + 50 alpha; rentang invers 50-100% D_ref.",
        },
        "aturan_fis1": {
            "rendah": {
                "tinggi": "tinggi", "sedang": "sedang", "rendah": "rendah",
                "tidak_diperlukan": "tidak_perlu",
            },
            "sedang": {
                "tinggi": "sedang", "sedang": "sedang", "rendah": "rendah",
                "tidak_diperlukan": "tidak_perlu",
            },
            "tinggi": {
                "tinggi": "tidak_perlu", "sedang": "tidak_perlu", "rendah": "tidak_perlu",
                "tidak_diperlukan": "tidak_perlu",
            },
        },
        "tabel": table,
        "acuan_ph": PH_ACUAN,
        "kalibrasi_dref": {
            "dasar_status_hara": "Rendah pada kelima fase",
            "z_lima_fase": z_values,
            "jumlah_z_persen": {"N": 271.2, "P": 300, "K": 500},
            "target_tahunan_g": {"N": 1150, "P": 490, "K": 1710},
            "dref_rumus": "D_ref,x = target_tahunan_x / (jumlah_Z_x / 100)",
            "hasil_dref_g_hara": DREF,
        },
        "catatan": [
            "Prioritas Rendah bukan lagi sinonim tidak perlu; pada status hara Rendah/Sedang konsekuennya Rendah dengan Z positif kecil.",
            "Status hara Tinggi dipetakan ke konsekuen Tidak perlu pada ketiga kelas prioritas biasa.",
            "Prioritas tidak_diperlukan pada P₂O₅ fase Prapanen merupakan pengecualian deterministik berdasarkan nilai P₂O₅ nol pada tabel satu bulan sebelum panen; fase ini didefinisikan sebagai jendela sekitar satu bulan sebelum panen sampai pemetikan pertama.",
            "D_ref merupakan kalibrasi matematis dari satu studi Monthong Thailand, bukan dosis per fase yang tervalidasi untuk kebun lokal.",
            "Keluaran Dolomit dan Belerang tetap indikatif dan memerlukan analisis tanah.",
        ],
    }
    raw = json.dumps(acuan, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
    json_path = ROOT / "tabel_acuan_v1_2.json"
    json_path.write_text(raw, encoding="utf-8")
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    (ROOT / "tabel_acuan_v1_2.sha256").write_text(
        f"{digest}  tabel_acuan_v1_2.json\n", encoding="utf-8"
    )

    sample = {}
    with (ROOT / "kasus_uji_acuan_v1_1.csv").open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            if row["hari"] not in sample:
                values = {hara: float(row[hara]) for hara in ("N", "P", "K")}
                sample[row["hari"]] = {
                    "hari": row["hari"],
                    **{hara: int(value) if value.is_integer() else value
                       for hara, value in values.items()},
                }
    with (ROOT / "kasus_uji_acuan_v1_2.csv").open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(["hari", "N", "P", "K", "fase", "hara", "nilai", "status",
                         "prioritas", "kategori_acuan", "g_hara_min", "g_hara_maks"])
        for row in list(sample.values())[:30]:
            for phase in PHASES:
                for hara in ("N", "P", "K"):
                    status = get_status(row[hara], hara)
                    consequent = RULES[(status.lower(), PRIORITAS[phase][hara])]
                    low, high = OUTPUT_RANGE[consequent]
                    writer.writerow([
                        row["hari"], row["N"], row["P"], row["K"], phase, hara,
                        row[hara], status, PRIORITAS[phase][hara], OUTPUT_NAME[consequent],
                        f"{low / 100 * DREF[hara]:.2f}",
                        f"{high / 100 * DREF[hara]:.2f}",
                    ])

    (ROOT / "kasus_uji_acuan_ph_v1_2.csv").write_bytes(
        (ROOT / "kasus_uji_acuan_ph_v1_1.csv").read_bytes()
    )
    print("Generated FIS-1 v1.2 reference table and 450 consistency cases:", digest)


if __name__ == "__main__":
    build()
