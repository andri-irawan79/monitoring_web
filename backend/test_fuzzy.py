"""Manual smoke test membership FIS-1/FIS-2."""
from fuzzy.membership import derajat_hara, derajat_ph
from fuzzy.parameter import DEFAULT

if __name__ == "__main__":
    print("Derajat hara N:", derajat_hara(20, DEFAULT.hara["N"]))
    print("Derajat pH:", derajat_ph(6.0, DEFAULT))
