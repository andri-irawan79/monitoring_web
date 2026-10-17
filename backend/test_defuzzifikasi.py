from fuzzy.tsukamoto import (
    fuzzifikasi,
    evaluate_phase,
    defuzzifikasi
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

print("Rule Aktif:")
print(hasil)

dosis = defuzzifikasi(
    hasil
)

print()
print("Dosis Akhir:")
print(dosis)