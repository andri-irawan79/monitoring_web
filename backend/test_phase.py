"""Manual smoke test untuk seluruh fase pada matrix v1.1."""
from fuzzy.rules import PHASES
from fuzzy.tsukamoto import hitung_rekomendasi

if __name__ == "__main__":
    for phase in PHASES:
        result = hitung_rekomendasi(40, 45, 30, 4.8, 100, phase, kelembapan_tanah=20)
        print(phase, result["doses_g"], result["corrections_g"])
