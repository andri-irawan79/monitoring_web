"""Manual smoke test rekomendasi untuk kelima fase."""
from fuzzy.tsukamoto import hitung_rekomendasi

if __name__ == "__main__":
    for phase in ("Vegetatif", "Pembungaan", "Pembuahan", "Panen", "Pascapanen"):
        result = hitung_rekomendasi(40, 45, 30, 6.0, 100, phase, kelembapan_tanah=20)
        print(phase, result["doses_g"], result["corrections_g"])
