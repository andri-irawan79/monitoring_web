from fuzzy.tsukamoto import (
    fuzzifikasi,
    hitung_alpha
)

from fuzzy.rules import RULES


fuzzy = fuzzifikasi(
    nitrogen=68,
    phosphorus=58,
    potassium=38,
    ph=6.3
)

rule = RULES[11]

print(rule)

alpha = hitung_alpha(
    rule,
    fuzzy
)

print(
    "Alpha:",
    alpha
)