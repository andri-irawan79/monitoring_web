"""Pengujian tabel acuan v1.0, v1.1, dan matriks prioritas v1.2."""
import csv
import hashlib
import json
import math
from pathlib import Path

from fuzzy.rules import FIS1_RULES, PHASES, PHASE_PRIORITY
from fuzzy.tsukamoto import hitung_rekomendasi

RISET = Path(__file__).resolve().parent.parent.parent / "riset"
SHA_V1_0 = "3f9e0b81a57f3f17ca2acd7ee9e0972669fd05b28c6ec899ed1f6612d6420eaf"
SHA_V1_1 = "9678404016a3b996bb03ddd62bdf03d1cc8a2c114b52505c08a0f9191e080f74"
SHA_V1_2 = "__TO_BE_SET__"


def _csv(name):
    with (RISET / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def test_tabel_acuan_v1_0_dan_v1_1_tetap_terkunci():
    for filename, checksum, recorded in (
        ("tabel_acuan_v1.json", SHA_V1_0, "tabel_acuan_v1.sha256"),
        ("tabel_acuan_v1_1.json", SHA_V1_1, "tabel_acuan_v1_1.sha256"),
    ):
        actual = hashlib.sha256((RISET / filename).read_bytes()).hexdigest()
        recorded_hash = (RISET / recorded).read_text(encoding="utf-8").split()[0]
        assert actual == recorded_hash == checksum


def test_tabel_acuan_v1_2_terkunci():
    actual = hashlib.sha256((RISET / "tabel_acuan_v1_2.json").read_bytes()).hexdigest()
    recorded = (RISET / "tabel_acuan_v1_2.sha256").read_text(encoding="utf-8").split()[0]
    assert actual == recorded == SHA_V1_2


def test_45_kombinasi_tabel_v1_2_sesuai_basis_aturan():
    reference = json.loads((RISET / "tabel_acuan_v1_2.json").read_text(encoding="utf-8"))
    assert len(reference["tabel"]) == 45
    output_name = {
        "tidak_perlu": "Tidak perlu",
        "rendah": "Rendah",
        "sedang": "Sedang",
        "tinggi": "Tinggi",
    }
    for row in reference["tabel"]:
        consequent = FIS1_RULES[(row["status"].lower(), row["prioritas"].lower())]
        assert row["kategori"] == output_name[consequent]

    assert PHASES == ("Pascapanen", "Vegetatif", "Prapembungaan", "Pembuahan", "Prapanen")
    assert PHASE_PRIORITY["Prapanen"]["P"] == "tidak_diperlukan"


def test_kesesuaian_450_kasus_terhadap_konsekuen_aturan_v1_2():
    output_name = {
        "tidak_perlu": "Tidak perlu",
        "rendah": "Rendah",
        "sedang": "Sedang",
        "tinggi": "Tinggi",
    }
    cases = _csv("kasus_uji_acuan_v1_2.csv")
    assert len(cases) == 450
    category_matches = 0

    for row in cases:
        values = {"N": 40.0, "P": 27.0, "K": 35.0}
        values[row["hara"]] = float(row["nilai"])
        result = hitung_rekomendasi(
            values["N"], values["P"], values["K"], 6.0, 100.0,
            row["fase"], kelembapan_tanah=20.0,
        )
        detail = result["fis1"][row["hara"]]["grouped"]
        dominant = max(detail, key=lambda item: item["alpha"])["consequent"]
        category_matches += output_name[dominant] == row["kategori_acuan"]
        z = result["z"][row["hara"].lower()]
        assert math.isfinite(z) and 0.0 <= z <= 100.0

    assert category_matches / len(cases) >= 0.90, (
        f"kesesuaian konsekuen dominan {category_matches}/{len(cases)}"
    )


def test_fis2_tetap_independen_dari_fase_dan_tidak_berubah():
    cases = _csv("kasus_uji_acuan_ph_v1_1.csv")
    assert len(cases) == 13
    transition_zone = lambda ph: 5.0 < ph < 5.5 or 6.5 < ph <= 7.25

    for row in cases:
        ph = float(row["ph"])
        results = [
            hitung_rekomendasi(31, 27, 35, ph, 100, phase, kelembapan_tanah=20)
            for phase in PHASES
        ]
        reference_correction = results[0]["corrections_g"]
        assert all(result["corrections_g"] == reference_correction for result in results)
        if not transition_zone(ph):
            for result in results:
                assert result["z"]["dolomit"] == results[0]["z"]["dolomit"]
                assert result["z"]["belerang"] == results[0]["z"]["belerang"]
