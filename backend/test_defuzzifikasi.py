"""Manual smoke test inferensi FIS-1 dan FIS-2."""
from fuzzy.tsukamoto import infer_fis1, infer_fis2

if __name__ == "__main__":
    print("FIS-1 Nitrogen:", infer_fis1("N", 68, "Vegetatif"))
    print("FIS-1 Fosfor:", infer_fis1("P", 58, "Vegetatif"))
    print("FIS-1 Kalium:", infer_fis1("K", 38, "Vegetatif"))
    print("FIS-2 pH:", infer_fis2(6.3))
