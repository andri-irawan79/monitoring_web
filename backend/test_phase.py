from fuzzy.tsukamoto import (
    fuzzifikasi,
    evaluate_phase
)

fuzzy = fuzzifikasi(
    nitrogen=68,
    phosphorus=58,
    potassium=38,
    ph=6.3
)

hasil = evaluate_phase(
    "Vegetatif",
    fuzzy
)

for h in hasil:

    print(h)