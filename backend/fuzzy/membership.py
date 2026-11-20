"""Fungsi keanggotaan FIS-1/FIS-2 berdasarkan ZIP acuan."""
from .parameter import DEFAULT, FuzzyParameters

def turun(x: float, a: float, b: float) -> float:
    if b <= a:
        raise ValueError("Parameter fungsi turun harus memenuhi b > a")
    if x <= a:
        return 1.0
    if x >= b:
        return 0.0
    return (b - x) / (b - a)

def naik(x: float, a: float, b: float) -> float:
    if b <= a:
        raise ValueError("Parameter fungsi naik harus memenuhi b > a")
    if x <= a:
        return 0.0
    if x >= b:
        return 1.0
    return (x - a) / (b - a)

def segitiga(x: float, a: float, c: float, b: float) -> float:
    if not a < c < b:
        raise ValueError("Parameter segitiga harus memenuhi a < c < b")
    if x <= a or x >= b:
        return 0.0
    return (x - a) / (c - a) if x <= c else (b - x) / (b - c)

def trapesium(x: float, a: float, b: float, c: float, d: float) -> float:
    if not a < b <= c < d:
        raise ValueError("Parameter trapesium harus memenuhi a < b <= c < d")
    if x <= a or x >= d:
        return 0.0
    if x < b:
        return (x - a) / (b - a)
    if x <= c:
        return 1.0
    return (d - x) / (d - c)

def derajat_hara(value: float, params: tuple[float, float, float]) -> dict[str, float]:
    a, c, b = params
    return {"rendah": turun(value, a, c), "sedang": segitiga(value, a, c, b),
            "tinggi": naik(value, c, b)}

def derajat_kelembapan(value: float, par: FuzzyParameters = DEFAULT) -> dict[str, float]:
    a, c, b = par.moisture
    return {"kering": turun(value, a, c), "optimal": segitiga(value, a, c, b),
            "basah": naik(value, c, b)}

def derajat_ph(value: float, par: FuzzyParameters = DEFAULT) -> dict[str, float]:
    return {"masam": turun(value, *par.ph["masam"]),
            "normal": trapesium(value, *par.ph["normal"]),
            "basa": naik(value, *par.ph["basa"])}

def fuzzifikasi(n: float, p: float, k: float, ph: float,
                kelembapan_tanah: float | None = None,
                par: FuzzyParameters = DEFAULT) -> dict[str, dict[str, float]]:
    """Kelembapan tanah opsional; jangan samakan dengan kelembapan udara."""
    values = {"N": derajat_hara(n, par.hara["N"]),
              "P": derajat_hara(p, par.hara["P"]),
              "K": derajat_hara(k, par.hara["K"]),
              "PH": derajat_ph(ph, par)}
    if kelembapan_tanah is not None:
        values["KELEMBAPAN_TANAH"] = derajat_kelembapan(kelembapan_tanah, par)
    return values

def kelas_tertinggi(values: dict[str, float]) -> str:
    # Urutan tie mengikuti urutan kategori pada ZIP acuan.
    return max(values, key=values.get)

def status_monitoring(n: float, p: float, k: float, ph: float,
                      kelembapan_tanah: float | None = None,
                      par: FuzzyParameters = DEFAULT) -> dict[str, str]:
    fuzzy = fuzzifikasi(n, p, k, ph, kelembapan_tanah, par)
    statuses = {"status_n": kelas_tertinggi(fuzzy["N"]).capitalize(),
                "status_p": kelas_tertinggi(fuzzy["P"]).capitalize(),
                "status_k": kelas_tertinggi(fuzzy["K"]).capitalize(),
                "status_ph": kelas_tertinggi(fuzzy["PH"]).capitalize()}
    if "KELEMBAPAN_TANAH" in fuzzy:
        statuses["status_kelembapan_tanah"] = kelas_tertinggi(fuzzy["KELEMBAPAN_TANAH"]).capitalize()
    return statuses
