"""Manual inspection nilai alpha FIS-1."""
from fuzzy.tsukamoto import infer_fis1

if __name__ == "__main__":
    result = infer_fis1("N", 68, "Vegetatif")
    for rule in result["rules"]:
        print(rule["rule_id"], "alpha=", rule["alpha"], "z=", rule["z"])
