"""Konversi keluaran Z FIS-1 menjadi dosis pupuk hara."""
import math
from typing import Any

from .parameter import DEFAULT, FuzzyParameters


def _round_dose(value: float, par: FuzzyParameters = DEFAULT) -> int:
    rounded = int(math.floor(value / par.rounding_step_g + 0.5) * par.rounding_step_g)
    return 0 if rounded < par.minimum_dose_g else rounded


def konversi_kebutuhan_hara(
    z_hara: dict[str, float],
    par: FuzzyParameters = DEFAULT,
) -> dict[str, Any]:
    """Konversi Z N/P/K (0–100) menjadi NPK 16-16-16, Urea, SP-36, dan KCl.

    Rumus serta kandungan pupuk mengikuti sumber ZIP acuan. Unit hasil dosis
    adalah gram per pohon per aplikasi; kesesuaian agronominya tetap perlu
    diverifikasi terhadap sumber D_ref dan basis satuan penelitian.
    """
    required = ("N", "P", "K")
    if any(key not in z_hara for key in required):
        raise ValueError("Nilai Z untuk N, P, dan K wajib tersedia")

    for key in required:
        value = float(z_hara[key])
        if not math.isfinite(value) or not 0.0 <= value <= 100.0:
            raise ValueError(f"Nilai Z {key} harus berada pada rentang 0 sampai 100")

    target = {
        nutrient: float(z_hara[nutrient]) / 100.0 * par.dref[nutrient]
        for nutrient in required
    }
    content = par.fertilizer_content
    npk_dose = (
        min(target.values()) / content["npk"]
        if all(float(z_hara[nutrient]) > 0 for nutrient in required)
        else 0.0
    )
    remaining = {
        nutrient: max(0.0, target[nutrient] - content["npk"] * npk_dose)
        for nutrient in required
    }
    doses = {
        "urea": _round_dose(remaining["N"] / content["urea"], par),
        "sp36": _round_dose(remaining["P"] / content["sp36"], par),
        "kcl": _round_dose(remaining["K"] / content["kcl"], par),
        "npk": _round_dose(npk_dose, par),
    }
    return {"target_hara_g": target, "remaining_hara_g": remaining, "doses_g": doses}
