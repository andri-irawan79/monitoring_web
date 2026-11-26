"""Manual smoke test evaluasi aturan tiap variabel."""
from fuzzy.tsukamoto import infer_fis1

if __name__ == "__main__":
    for variable, value in (("N", 68), ("P", 58), ("K", 38)):
        result = infer_fis1(variable, value, "Vegetatif")
        print(variable, "priority=", result["priority"], "rules=", result["rules"])
