"""Manual smoke test fungsi keluaran Tsukamoto."""
from fuzzy.tsukamoto import z_keluaran

if __name__ == "__main__":
    alpha = 0.7
    print("z rendah:", z_keluaran("rendah", alpha))
    print("z sedang:", z_keluaran("sedang", alpha))
    print("z tinggi:", z_keluaran("tinggi", alpha))
