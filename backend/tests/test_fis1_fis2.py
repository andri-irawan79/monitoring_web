import pytest

from fuzzy.parameter import DEFAULT, get_parameters
from fuzzy.membership import derajat_hara, derajat_ph, status_monitoring
from fuzzy.tsukamoto import hitung_rekomendasi


def test_contoh_manual_vegetatif_sesuai_zip():
    result = hitung_rekomendasi(40, 45, 30, 6.0, 100, "Vegetatif", kelembapan_tanah=20)
    assert result["doses_g"] == {"urea": 190, "sp36": 85, "kcl": 0, "npk": 0}
    assert result["z"]["n"] == 15.0
    assert round(result["z"]["p"], 1) == 12.8
    assert result["z"]["k"] == 0.0


def test_contoh_manual_pascapanen_sesuai_zip():
    result = hitung_rekomendasi(10, 10, 15, 6.0, 100, "Pascapanen", kelembapan_tanah=20)
    assert result["doses_g"] == {"urea": 360, "sp36": 0, "kcl": 510, "npk": 765}


def test_fase_panen_tidak_menghasilkan_koreksi_ph():
    result = hitung_rekomendasi(5, 5, 5, 6.0, 100, "Panen")
    assert result["corrections_g"] == {"dolomit": None, "belerang": None}
    assert any("pemupukan tidak dianjurkan" in note for note in result["notes"])


def test_fis2_merekomendasikan_dolomit_untuk_ph_masam():
    result = hitung_rekomendasi(35, 30, 35, 4.8, 100, "Vegetatif")
    assert result["z"]["dolomit"] > 0
    assert result["corrections_g"]["dolomit"][1] > 0


def test_profil_b_dapat_dipilih():
    result = hitung_rekomendasi(15, 15, 87.5, 6.0, 100, "Pembuahan", par=get_parameters("B"))
    assert result["profile"] == "B"
    assert set(result["doses_g"]) == {"urea", "sp36", "kcl", "npk"}


def test_derajat_keanggotaan_berada_di_rentang_nol_satu():
    for membership in (
        derajat_hara(40, DEFAULT.hara["N"]),
        derajat_ph(6.1, DEFAULT),
    ):
        assert all(0.0 <= degree <= 1.0 for degree in membership.values())


def test_kelembapan_udara_tidak_dianggap_sebagai_kelembapan_tanah():
    # Panggilan tanpa soil_moisture tidak membuat status tanah fiktif.
    result = hitung_rekomendasi(40, 45, 30, 6.0, 100, "Vegetatif")
    assert result["soil_moisture_available"] is False
    assert "KELEMBAPAN_TANAH" not in result["fuzzy_values"]


def test_fase_tidak_dikenal_ditolak():
    with pytest.raises(ValueError, match="Fase tidak dikenal"):
        hitung_rekomendasi(40, 45, 30, 6.0, 100, "Berbunga")


def test_status_monitoring_memakai_himpunan_fuzzy_yang_sama():
    status = status_monitoring(10, 27, 60, 4.8)
    assert status == {
        "status_n": "Rendah",
        "status_p": "Sedang",
        "status_k": "Tinggi",
        "status_ph": "Masam",
    }
