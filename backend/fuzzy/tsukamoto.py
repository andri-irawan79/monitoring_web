"""Engine FIS-1 (kebutuhan N/P/K) dan FIS-2 (koreksi pH).
Mesin murni Python; logika agregasi dan konversi dosis mengikuti ZIP acuan.
"""
from __future__ import annotations
import math
from typing import Any

from .membership import fuzzifikasi, kelas_tertinggi, derajat_hara, derajat_ph
from .parameter import DEFAULT, FuzzyParameters
from .rules import FIS1_RULES, FIS2_RULES, PHASES, PHASE_PRIORITY

def z_keluaran(kelas: str, alpha: float) -> float:
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("Alpha harus berada pada rentang 0 sampai 1")
    if kelas == "rendah":
        return 10.0 * (1.0 - alpha)
    if kelas == "sedang":
        return 50.0 * alpha
    if kelas == "tinggi":
        return 50.0 + 50.0 * alpha
    raise ValueError(f"Kelas keluaran tidak dikenal: {kelas}")

def tsukamoto(active_rules: list[tuple[float, str]], minimum_z: float = 10.0) -> dict[str, Any]:
    """Gabungkan alpha per konsekuen (jumlah dibatasi 1), lalu defuzzifikasi."""
    grouped: dict[str, float] = {}
    for alpha, consequent in active_rules:
        if not math.isfinite(alpha) or not 0.0 <= alpha <= 1.0:
            raise ValueError("Derajat aktivasi rule harus berada pada rentang 0 sampai 1")
        if alpha > 0:
            grouped[consequent] = min(1.0, grouped.get(consequent, 0.0) + alpha)
    numerator = denominator = 0.0
    grouped_rows = []
    for consequent, alpha in grouped.items():
        z = z_keluaran(consequent, alpha)
        numerator += alpha * z
        denominator += alpha
        grouped_rows.append({"consequent": consequent, "alpha": alpha,
                             "z": z, "alpha_z": alpha * z})
    raw_z = numerator / denominator if denominator else 0.0
    z = 0.0 if raw_z < minimum_z else raw_z
    return {"z": z, "raw_z": raw_z, "numerator": numerator,
            "denominator": denominator, "grouped": grouped_rows}

def infer_fis1(variable: str, value: float, phase: str,
               par: FuzzyParameters = DEFAULT) -> dict[str, Any]:
    if phase not in PHASE_PRIORITY:
        raise ValueError(f"Fase tidak dikenal: {phase}")
    if variable not in ("N", "P", "K"):
        raise ValueError(f"Variabel FIS-1 tidak dikenal: {variable}")
    membership = derajat_hara(value, par.hara[variable])
    priority = PHASE_PRIORITY[phase][variable]
    rule_rows = []
    active = []
    for status, alpha in membership.items():
        consequent = FIS1_RULES[(status, priority)]
        rule_rows.append({
            "rule_id": f"FIS1-{variable}-{status.upper()}",
            "variable": variable,
            "condition": f"{status} AND prioritas fase {priority}",
            "status_hara": status,
            "prioritas_fase": priority,
            "consequent": consequent,
            "alpha": alpha,
            "z": z_keluaran(consequent, alpha) if alpha > 0 else None,
            "active": alpha > 0,
        })
        active.append((alpha, consequent))
    return {"variable": variable, "input": value, "priority": priority,
            "membership": membership, "rules": rule_rows,
            **tsukamoto(active, par.minimum_z)}

def infer_fis2(ph: float, par: FuzzyParameters = DEFAULT) -> dict[str, Any]:
    membership = derajat_ph(ph, par)
    outputs = {}
    all_rules = []
    for output_index, output_name in enumerate(("dolomit", "belerang")):
        rows = []
        active = []
        for status, alpha in membership.items():
            consequent = FIS2_RULES[status][output_index]
            row = {"rule_id": f"FIS2-{output_name.upper()}-{status.upper()}",
                   "variable": "PH", "condition": status, "status_ph": status,
                   "consequent": consequent, "alpha": alpha,
                   "z": z_keluaran(consequent, alpha) if alpha > 0 else None,
                   "active": alpha > 0, "output": output_name}
            rows.append(row)
            all_rules.append(row)
            active.append((alpha, consequent))
        outputs[output_name] = {"membership": membership, "rules": rows,
                                **tsukamoto(active, par.minimum_z)}
    return {"input": ph, "membership": membership, "outputs": outputs, "rules": all_rules}

def _round_dose(value: float, par: FuzzyParameters) -> int:
    rounded = int(math.floor(value / par.rounding_step_g + 0.5) * par.rounding_step_g)
    return 0 if rounded < par.minimum_dose_g else rounded

def hitung_rekomendasi(n: float, p: float, k: float, ph: float,
                       hujan: float, fase: str, par: FuzzyParameters = DEFAULT,
                       kelembapan_tanah: float | None = None) -> dict[str, Any]:
    """Hasil paket pupuk hara + koreksi pH menurut algoritma ZIP acuan."""
    if fase not in PHASES:
        raise ValueError(f"Fase tidak dikenal: {fase}")
    for label, value in (("N", n), ("P", p), ("K", k), ("pH", ph), ("curah hujan", hujan)):
        if value is None:
            continue
        if not math.isfinite(float(value)):
            raise ValueError(f"Nilai {label} harus berupa angka terbatas")
        if value < 0:
            raise ValueError(f"Nilai {label} tidak boleh negatif")
    if ph > 14:
        raise ValueError("Nilai pH harus berada pada rentang 0 sampai 14")
    if kelembapan_tanah is not None and not 0 <= kelembapan_tanah <= 100:
        raise ValueError("Kelembapan tanah harus berada pada rentang 0 sampai 100")

    memberships = fuzzifikasi(n, p, k, ph, kelembapan_tanah, par)
    fis1 = {variable: infer_fis1(variable, value, fase, par)
            for variable, value in (("N", n), ("P", p), ("K", k))}
    fis2 = infer_fis2(ph, par)
    z = {"N": fis1["N"]["z"], "P": fis1["P"]["z"], "K": fis1["K"]["z"],
         "dolomit": fis2["outputs"]["dolomit"]["z"],
         "belerang": fis2["outputs"]["belerang"]["z"]}

    target_hara = {h: z[h] / 100.0 * par.dref[h] for h in ("N", "P", "K")}
    content = par.fertilizer_content
    npk_dose = (min(target_hara.values()) / content["npk"]
                if all(z[h] > 0 for h in ("N", "P", "K")) else 0.0)
    remaining = {h: max(0.0, target_hara[h] - content["npk"] * npk_dose)
                 for h in ("N", "P", "K")}
    doses = {"urea": _round_dose(remaining["N"] / content["urea"], par),
             "sp36": _round_dose(remaining["P"] / content["sp36"], par),
             "kcl": _round_dose(remaining["K"] / content["kcl"], par),
             "npk": _round_dose(npk_dose, par)}

    corrections = {"dolomit": None, "belerang": None}
    if fase != "Panen":
        corrections = {
            "dolomit": [round(z["dolomit"] / 100.0 * par.dolomite_range[0]),
                        round(z["dolomit"] / 100.0 * par.dolomite_range[1])],
            "belerang": [round(z["belerang"] / 100.0 * par.sulfur_range[0]),
                         round(z["belerang"] / 100.0 * par.sulfur_range[1])],
        }

    notes = []
    if ph < par.ph_lower_optimal or ph > par.ph_upper_optimal:
        notes.append("pH di luar kisaran optimal; koreksi pH lebih dahulu")
    if "KELEMBAPAN_TANAH" in memberships:
        moisture_class = kelas_tertinggi(memberships["KELEMBAPAN_TANAH"])
        if moisture_class == "kering":
            notes.append("pastikan tanah cukup lembap")
        elif moisture_class == "basah":
            notes.append("tunda atau pecahkan dosis")
    if hujan > par.high_rainfall_mm:
        notes.append("pecahkan dosis (curah hujan tinggi)")
    if not any(doses.values()):
        notes.append("pemupukan tidak dianjurkan pada kondisi atau fase ini")

    active_rules = [row for result in fis1.values() for row in result["rules"] if row["active"]]
    active_rules.extend(row for row in fis2["rules"] if row["active"])
    return {
        "profile": par.profile,
        "phase": fase,
        "soil_moisture_available": kelembapan_tanah is not None,
        "fuzzy_values": memberships,
        "fis1": fis1,
        "fis2": fis2,
        "z": {key.lower(): round(value, 4) for key, value in z.items()},
        "target_hara_g": {key: round(value, 4) for key, value in target_hara.items()},
        "remaining_hara_g": {key: round(value, 4) for key, value in remaining.items()},
        "doses_g": doses,
        "corrections_g": corrections,
        "notes": notes,
        "active_rules": active_rules,
        "parameter_warnings": [
            "D_ref dan kadar pupuk mengikuti parameter pada ZIP acuan dan harus diverifikasi sumber agronominya.",
            "Rentang dosis Dolomit dan Belerang masih bersifat indikatif menurut ZIP acuan.",
        ],
    }
