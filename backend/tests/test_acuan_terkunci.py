"""Pengujian tabel acuan v1.0 terkunci dan revisi matriks fase v1.1."""
import csv
import hashlib
from pathlib import Path

from fuzzy.rules import PHASES, PHASE_PRIORITY
from fuzzy.tsukamoto import hitung_rekomendasi

RISET = Path(__file__).resolve().parent.parent.parent / "riset"
SHA_V1_0 = "3f9e0b81a57f3f17ca2acd7ee9e0972669fd05b28c6ec899ed1f6612d6420eaf"
SHA_V1_1 = "87b39e70a75e423324860120d459795e3580b8304f698382fa5e9b085709f4fe"


def _csv(name):
    with (RISET / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def _category(z):
    return "Tidak perlu" if z < 10 else "Sedang" if z < 75 else "Tinggi"


def test_tabel_acuan_v1_0_tetap_terkunci():
    actual_file_hash = hashlib.sha256((RISET / "tabel_acuan_v1.json").read_bytes()).hexdigest()
    recorded_hash = (RISET / "tabel_acuan_v1.sha256").read_text(encoding="utf-8").split()[0]
    assert recorded_hash == SHA_V1_0
    assert actual_file_hash == SHA_V1_0


def test_tabel_acuan_v1_1_terkunci():
    actual_file_hash = hashlib.sha256((RISET / "tabel_acuan_v1_1.json").read_bytes()).hexdigest()
    recorded_hash = (RISET / "tabel_acuan_v1_1.sha256").read_text(encoding="utf-8").split()[0]
    assert recorded_hash == SHA_V1_1
    assert actual_file_hash == SHA_V1_1


def test_matriks_fase_v1_1_sesuai_basis_aturan():
    assert PHASES == ("Pascapanen", "Vegetatif", "Prapembungaan", "Pembuahan", "Prapanen")
    assert PHASE_PRIORITY == {
        "Pascapanen": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
        "Vegetatif": {"N": "tinggi", "P": "sedang", "K": "tinggi"},
        "Prapembungaan": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
        "Pembuahan": {"N": "sedang", "P": "sedang", "K": "tinggi"},
        "Prapanen": {"N": "tinggi", "P": "rendah", "K": "tinggi"},
    }


def test_kesesuaian_450_kasus_hara_v1_1():
    limits = {
        "Tidak perlu": (0.0, 0.0),
        "Sedang": (25.0, 75.0),
        "Tinggi": (75.0, 100.0),
    }
    cases = _csv("kasus_uji_acuan_v1_1.csv")
    assert len(cases) == 450
    category_matches = 0
    within_reference_band = 0

    for row in cases:
        values = {"N": 40.0, "P": 27.0, "K": 35.0}
        values[row["hara"]] = float(row["nilai"])
        z = hitung_rekomendasi(
            values["N"], values["P"], values["K"], 6.0, 100.0,
            row["fase"], kelembapan_tanah=20.0,
        )["z"][row["hara"].lower()]
        expected = row["kategori_acuan"]
        category_matches += _category(z) == expected
        low, high = limits[expected]
        within_reference_band += ((z == 0.0) if expected == "Tidak perlu"
                                  else (low - 1e-9 <= z <= high + 1e-9))

    assert category_matches / len(cases) >= 0.90, (
        f"kesesuaian kategori {category_matches}/{len(cases)}"
    )
    assert within_reference_band / len(cases) >= 0.90, (
        f"keluaran dalam rentang acuan {within_reference_band}/{len(cases)}"
    )


def test_fis2_tidak_bergantung_pada_fase_dan_dilaporkan_terpisah():
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
        assert reference_correction["dolomit"] is not None
        assert reference_correction["belerang"] is not None

        dolomite = "Diperlukan" if results[0]["z"]["dolomit"] > 0 else "Tidak diperlukan"
        sulfur = "Diperlukan" if results[0]["z"]["belerang"] > 0 else "Tidak diperlukan"
        if not transition_zone(ph):
            assert dolomite == row["dolomit_acuan"]
            assert sulfur == row["belerang_acuan"]
