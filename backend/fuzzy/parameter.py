"""Parameter FIS dari ZIP acuan skripsi-durian.
Profil A/B, D_ref, kadar pupuk dan batas lain mengikuti riset/fuzzy_tsukamoto.py.
D_ref v1.2 memisahkan konsekuen Tidak perlu dan Rendah; nilainya dikalibrasi dari satu studi Monthong Thailand, bukan dosis lapangan tervalidasi. Rentang Dolomit/Belerang tetap indikatif.
"""
from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True)
class FuzzyParameters:
    profile: str
    hara: Mapping[str, tuple[float, float, float]]
    moisture: tuple[float, float, float]
    ph: Mapping[str, tuple[float, ...]]
    dref: Mapping[str, float]
    fertilizer_content: Mapping[str, float]
    dolomite_range: tuple[int, int] = (1000, 3000)
    sulfur_range: tuple[int, int] = (350, 700)
    minimum_z: float = 10.0
    rounding_step_g: int = 5
    minimum_dose_g: int = 20
    high_rainfall_mm: float = 200.0
    ph_lower_optimal: float = 5.5
    ph_upper_optimal: float = 6.5

_PROFILE_HARA = {
    "A": {"N": (15.0, 31.0, 49.0), "P": (17.0, 27.0, 60.0), "K": (27.0, 35.0, 47.0)},
    "B": {"N": (10.0, 15.0, 20.0), "P": (10.0, 15.5, 21.0), "K": (50.0, 87.5, 125.0)},
}

def get_parameters(profile: str = "A") -> FuzzyParameters:
    normalized = (profile or "A").upper()
    if normalized not in _PROFILE_HARA:
        raise ValueError("Profil parameter harus A atau B")
    return FuzzyParameters(
        profile=normalized,
        hara=_PROFILE_HARA[normalized],
        moisture=(15.0, 20.0, 25.0),
        ph={"masam": (4.5, 5.5), "normal": (4.5, 5.5, 6.5, 8.0), "basa": (6.5, 8.0)},
        dref={"N": 424.0412979351032, "P": 163.33333333333334, "K": 342.0},
        fertilizer_content={"urea": 0.46, "sp36": 0.36, "kcl": 0.60, "npk": 0.16},
    )

DEFAULT = get_parameters("A")
