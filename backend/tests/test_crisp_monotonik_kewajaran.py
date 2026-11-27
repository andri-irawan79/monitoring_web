"""Uji pembanding crisp, perilaku monotonik lokal, dan penapisan dosis lima fase."""
import csv
from pathlib import Path

from fuzzy.parameter import DEFAULT
from fuzzy.rules import FIS1_RULES, PHASES, PHASE_PRIORITY
from fuzzy.tsukamoto import hitung_rekomendasi

RISET = Path(__file__).resolve().parent.parent.parent / "riset"
RENTANG = {"N": (0, 140), "P": (5, 145), "K": (5, 205)}
SKOR = {"tidak_perlu": 0.0, "rendah": 10.6, "sedang": 50.0, "tinggi": 100.0}


def _z(hara, x, fase):
    values = {"N": 31.0, "P": 27.0, "K": 35.0}
    values[hara] = float(x)
    return hitung_rekomendasi(
        values["N"], values["P"], values["K"], 6.0, 100.0, fase,
        kelembapan_tanah=20.0,
    )["z"][hara.lower()]


def _crisp_z(hara, x, fase):
    a, c, b = DEFAULT.hara[hara]
    status = "rendah" if x <= a else "tinggi" if x >= b else "sedang"
    consequent = FIS1_RULES[(status, PHASE_PRIORITY[fase][hara])]
    return SKOR[consequent]


def test_fuzzy_lebih_mulus_daripada_crisp():
    fuzzy_jumps = crisp_jumps = 0
    max_fuzzy_jump = 0.0
    for hara, (low, high) in RENTANG.items():
        for phase in PHASES:
            fuzzy_values = [_z(hara, value, phase) for value in range(low, high + 1)]
            crisp_values = [_crisp_z(hara, value, phase) for value in range(low, high + 1)]
            fuzzy_delta = [
                abs(fuzzy_values[i + 1] - fuzzy_values[i])
                for i in range(len(fuzzy_values) - 1)
            ]
            crisp_delta = [
                abs(crisp_values[i + 1] - crisp_values[i])
                for i in range(len(crisp_values) - 1)
            ]
            fuzzy_jumps += sum(value > 25.0 for value in fuzzy_delta)
            crisp_jumps += sum(value > 25.0 for value in crisp_delta)
            max_fuzzy_jump = max(max_fuzzy_jump, max(fuzzy_delta, default=0.0))
    assert fuzzy_jumps == 0 and crisp_jumps > 0 and max_fuzzy_jump < 25.0, (
        fuzzy_jumps, crisp_jumps, max_fuzzy_jump
    )


def test_kenaikan_lokal_z_dibatasi_5_poin_persen():
    total = 0
    for nutrient, (low, high) in RENTANG.items():
        for phase in PHASES:
            values = [_z(nutrient, value, phase) for value in range(low, high + 1)]
            increases = [
                values[i + 1] - values[i]
                for i in range(len(values) - 1)
                if values[i + 1] > values[i] + 1e-3
            ]
            assert all(delta <= 5.0 for delta in increases), (
                nutrient, phase, max(increases, default=0.0)
            )
            total += len(increases)
    assert total == 22, f"jumlah kenaikan lokal v1.2 berubah menjadi {total}"


KISARAN = {"N": (649, 1800), "P": (490, 1560), "K": (717, 4000)}
KANDUNGAN = {"urea": 0.46, "sp36": 0.36, "kcl": 0.60, "npk": 0.16}


def test_kewajaran_dosis_tahunan_10_skenario():
    with (RISET / "skenario_uji.csv").open(newline="", encoding="utf-8") as source:
        data = {row["id"]: row for row in csv.DictReader(source)}
    scenario_ids = ["SK-19", "SK-20", "SK-21", "SK-22", "SK-23",
                    "SK-24", "SK-05", "SK-07", "SK-11", "SK-17"]
    annual = {}
    for scenario_id in scenario_ids:
        row = data[scenario_id]
        total = {"N": 0.0, "P": 0.0, "K": 0.0}
        for phase in PHASES:
            doses = hitung_rekomendasi(
                float(row["N"]), float(row["P"]), float(row["K"]),
                float(row["ph"]), float(row["rainfall"]), phase,
                kelembapan_tanah=float(row["soil_moisture"]),
            )["doses_g"]
            total["N"] += doses["urea"] * KANDUNGAN["urea"] + doses["npk"] * KANDUNGAN["npk"]
            total["P"] += doses["sp36"] * KANDUNGAN["sp36"] + doses["npk"] * KANDUNGAN["npk"]
            total["K"] += doses["kcl"] * KANDUNGAN["kcl"] + doses["npk"] * KANDUNGAN["npk"]
        annual[scenario_id] = total

    acceptable = 0
    for scenario_id, total in annual.items():
        passed = all(total[nutrient] <= KISARAN[nutrient][1] for nutrient in total)
        if scenario_id == "SK-19":
            passed = passed and all(
                KISARAN[nutrient][0] * 0.98 <= total[nutrient] <= KISARAN[nutrient][1]
                for nutrient in total
            )
        if scenario_id == "SK-21":
            passed = passed and all(total[nutrient] < annual["SK-19"][nutrient] for nutrient in total)
        acceptable += passed

    assert acceptable / len(scenario_ids) >= 0.80, f"skenario wajar {acceptable}/10"
