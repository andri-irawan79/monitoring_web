"""Paritas mesin aplikasi dengan implementasi acuan mandiri di riset/ (600 baris buah x 5 fase x profil A dan B)."""
from pathlib import Path

import pandas as pd
import pytest

from fuzzy.parameter import get_parameters
from fuzzy.tsukamoto import hitung_rekomendasi

REPO = Path(__file__).resolve().parent.parent.parent
FASE = ("Pascapanen", "Vegetatif", "Prapembungaan", "Pembuahan", "Prapanen")
BUAH = ["banana", "coconut", "mango", "orange", "papaya", "pomegranate"]

pytestmark = pytest.mark.skipif(not (REPO / "Crop_recommendationV2.csv").exists(), reason="dataset tidak ada di akar repo")


def _buah():
    d = pd.read_csv(REPO / "Crop_recommendationV2.csv")
    b = d[d.label.isin(BUAH)]
    assert len(b) == 600
    return b


@pytest.mark.parametrize("profil", ["A", "B"])
def test_paritas_600_baris_x_5_fase(profil):
    import fuzzy_tsukamoto as acuan
    par_acuan = acuan.PROFIL_A if profil == "A" else acuan.PROFIL_B
    par_app = get_parameters(profil)
    beda = []
    for _, r in _buah().iterrows():
        for fase in FASE:
            a = acuan.rekomendasi(r.N, r.P, r.K, r.ph, r.soil_moisture, r.rainfall, fase, profil=par_acuan)
            b = hitung_rekomendasi(r.N, r.P, r.K, r.ph, r.rainfall, fase, par_app, kelembapan_tanah=r.soil_moisture)
            ok = a["dosis"] == b["doses_g"] and a["catatan"] == b["notes"]
            for h in "NPK":
                ok = ok and abs(a["Z"][h] - b["z"][h.lower()]) < 1e-3           # mesin aplikasi membulatkan Z ke 4 desimal
            ok = ok and list(a["koreksi"]["dolomit"]) == b["corrections_g"]["dolomit"]
            ok = ok and list(a["koreksi"]["belerang"]) == b["corrections_g"]["belerang"]
            if not ok:
                beda.append((profil, fase, r.N, r.P, r.K))
    assert not beda, f"{len(beda)} kasus berbeda, contoh: {beda[:3]}"
