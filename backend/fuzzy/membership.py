# =====================================
# NITROGEN
# =====================================

def n_rendah(x):

    if x <= 30:
        return 1

    elif 30 < x < 55:
        return (55 - x) / (55 - 30)

    return 0


def n_sedang(x):

    if x <= 40 or x >= 120:
        return 0

    elif 40 < x <= 80:
        return (x - 40) / (80 - 40)

    elif 80 < x < 120:
        return (120 - x) / (120 - 80)

    return 0


def n_tinggi(x):

    if x <= 80:
        return 0

    elif 80 < x < 120:
        return (x - 80) / (120 - 80)

    return 1


# =====================================
# FOSFOR
# =====================================

def p_rendah(x):

    if x <= 25:
        return 1

    elif 25 < x < 50:
        return (50 - x) / (50 - 25)

    return 0


def p_sedang(x):

    if x <= 20 or x >= 100:
        return 0

    elif 20 < x <= 60:
        return (x - 20) / (60 - 20)

    elif 60 < x < 100:
        return (100 - x) / (100 - 60)

    return 0


def p_tinggi(x):

    if x <= 60:
        return 0

    elif 60 < x < 100:
        return (x - 60) / (100 - 60)

    return 1


# =====================================
# KALIUM
# =====================================

def k_rendah(x):

    if x <= 75:
        return 1

    elif 75 < x < 100:
        return (100 - x) / (100 - 75)

    return 0


def k_sedang(x):

    if x <= 50 or x >= 220:
        return 0

    elif 50 < x <= 150:
        return (x - 50) / (150 - 50)

    elif 150 < x < 220:
        return (220 - x) / (220 - 150)

    return 0


def k_tinggi(x):

    if x <= 150:
        return 0

    elif 150 < x < 220:
        return (x - 150) / (220 - 150)

    return 1


# =====================================
# PH
# =====================================

def ph_asam(x):

    if x <= 4.5:
        return 1

    elif 4.5 < x < 5.5:
        return (5.5 - x)

    return 0


def ph_normal(x):

    if x <= 5 or x >= 7:
        return 0

    elif 5 < x <= 6:
        return (x - 5)

    elif 6 < x < 7:
        return (7 - x)

    return 0


def ph_basa(x):

    if x <= 6.5:
        return 0

    elif 6.5 < x < 8:
        return (x - 6.5) / (8 - 6.5)

    return 1