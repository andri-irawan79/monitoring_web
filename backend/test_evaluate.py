from fuzzy.tsukamoto import evaluate_rules

rules = evaluate_rules(
    "Vegetatif"
)

print(
    "Jumlah Rule Vegetatif:"
)

print(
    len(rules)
)

print(
    rules[0]
)