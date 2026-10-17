def koreksi_varietas(
    dosis,
    varietas_id
):

    # Montong
    if varietas_id == 1:
        return dosis

    # Musang King (+10%)
    elif varietas_id == 2:
        return dosis * 1.10

    # Bawor (+5%)
    elif varietas_id == 3:
        return dosis * 1.05

    return dosis