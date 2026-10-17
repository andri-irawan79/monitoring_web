from fuzzy.rules import RULES
from fuzzy.membership import *

def z_rendah(alpha):

    return 2 - (alpha * 2)


def z_tinggi(alpha):

    return 3 + (alpha * 3)

def get_z(output, alpha):

    if output == "rendah":
        return z_rendah(alpha)

    if output == "tinggi":
        return z_tinggi(alpha)

    if output == "sedang":
        return 2.5
    
def alpha_predikat(values):

    return min(values)

def evaluate_rules(fase):

    active_rules = []

    for rule in RULES:

        if rule["fase"] == fase:

            active_rules.append(rule)

    return active_rules

def hitung_alpha(rule, fuzzy_values):

    nilai = []

    for variabel, label in rule["conditions"]:

        nilai.append(
            fuzzy_values[variabel][label]
        )

    return min(nilai)

def fuzzifikasi(
    nitrogen,
    phosphorus,
    potassium,
    ph
):

    return {

        "N": {
                "rendah": n_rendah(nitrogen),
                "sedang": n_sedang(nitrogen),
                "tinggi": n_tinggi(nitrogen)
            },

        "P": {
                "rendah": p_rendah(phosphorus),
                "sedang": p_sedang(phosphorus),
                "tinggi": p_tinggi(phosphorus)
            },

        "K": {
                "rendah": k_rendah(potassium),
                "sedang": k_sedang(potassium),
                "tinggi": k_tinggi(potassium)
            },

        "PH": {
            "asam": ph_asam(ph),
            "normal": ph_normal(ph),
            "basa": ph_basa(ph)
        }
    }

def evaluate_phase(
    fase,
    fuzzy_values
):

    hasil = []

    active_rules = evaluate_rules(
        fase
    )

    for rule in active_rules:

        alpha = hitung_alpha(
            rule,
            fuzzy_values
        )

        if alpha > 0:

            rule_result = {

                "rule_id": rule["id"],

                "fase": rule["fase"],

                "conditions": rule["conditions"],

                "pupuk": rule["pupuk"],

                "output": rule["output"],

                "alpha": round(alpha, 4)

            }

            # Hitung nilai z untuk rule ini
            rule_result["z"] = round(
                calculate_z(rule_result),
                4
            )

            hasil.append(
                rule_result
            )

    return hasil

def calculate_z(rule_result):

    alpha = rule_result["alpha"]

    return get_z(
        rule_result["output"],
        alpha
    )

def defuzzifikasi(results):

    sum_alpha = 0

    sum_alpha_z = 0

    for r in results:

        z = r["z"]

        alpha = r["alpha"]

        sum_alpha += alpha

        sum_alpha_z += alpha * z

    hasil = 0

    if sum_alpha > 0:

        hasil = sum_alpha_z / sum_alpha

    return {

        "alpha": round(sum_alpha, 4),

        "alpha_z": round(sum_alpha_z, 4),

        "hasil": round(hasil, 4)

    }