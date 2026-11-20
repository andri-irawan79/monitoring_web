"""Manual smoke test fuzzifikasi FIS-1/FIS-2."""
from fuzzy.tsukamoto import hitung_rekomendasi

if __name__ == "__main__":
    result = hitung_rekomendasi(68, 58, 38, 6.3, 100, "Vegetatif", kelembapan_tanah=20)
    print("Fuzzy values:", result["fuzzy_values"])
