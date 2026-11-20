"""Manual inspection basis aturan FIS-1/FIS-2."""
from fuzzy.rules import FIS1_RULES, FIS2_RULES, PHASE_PRIORITY

if __name__ == "__main__":
    print("Jumlah kombinasi aturan FIS-1:", len(FIS1_RULES))
    print("Prioritas fase:", PHASE_PRIORITY)
    print("Aturan FIS-2:", FIS2_RULES)
