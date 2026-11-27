import math

import pytest

from fuzzy.parameter import DEFAULT, get_parameters
from fuzzy.membership import derajat_hara, derajat_ph, derajat_kelembapan, status_monitoring
from fuzzy.rules import PHASES, PHASE_PRIORITY
from fuzzy.tsukamoto import hitung_rekomendasi


def test_lima_fase_dan_matriks_prioritas_v1_1():
    assert PHASES == ("Pascapanen", "Vegetatif", "Prapembungaan", "Pembuahan", "Prapanen")
    assert PHASE_PRIORITY == {
        "Pascapanen": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
        "Vegetatif": {"N": "tinggi", "P": "sedang", "K": "tinggi"},
        "Prapembungaan": {"N": "rendah", "P": "tinggi", "K": "tinggi"},
        "Pembuahan": {"N": "sedang", "P": "sedang", "K": "tinggi"},
        "Prapanen": {"N": "tinggi", "P": "rendah", "K": "tinggi"},
    }


def test_dref_v1_1_terkalibrasi_dari_target_tahunan():
    assert DEFAULT.dref["N"] == 460.0
    assert DEFAULT.dref["P"] == pytest.approx(490 / 3)
    assert DEFAULT.dref["K"] == 342.0


def test_contoh_manual_vegetatif_v1_1():
    result = hitung_rekomendasi(40, 45, 30, 6.0, 100, "Vegetatif", kelembapan_tanah=20)
    assert result["z"]["n"] == pytest.approx(15.0)
    assert result["z"]["p"] == pytest.approx(12.8099, abs=1e-3)
    assert result["z"]["k"] == pytest.approx(57.8125)
    assert result["doses_g"] == {"urea": 105, "sp36": 0, "kcl": 295, "npk": 130}


def test_fis2_berlaku_pada_seluruh_fase():
    results = {
        phase: hitung_rekomendasi(35, 30, 35, 4.8, 100, phase)["corrections_g"]
        for phase in PHASES
    }
    assert len({tuple(results[p]["dolomit"]) for p in PHASES}) == 1
    assert len({tuple(results[p]["belerang"]) for p in PHASES}) == 1
    assert all(results[p]["dolomit"][1] > 0 for p in PHASES)
    assert all(results[p]["belerang"] == [0, 0] for p in PHASES)


def test_pra_panen_bukan_kondisi_nol_otomatis():
    result = hitung_rekomendasi(0, 5, 5, 6.0, 100, "Prapanen")
    assert result["z"]["n"] == 100
    assert result["z"]["p"] == 0
    assert result["z"]["k"] == 100
    assert any(result["doses_g"].values())


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
    result = hitung_rekomendasi(40, 45, 30, 6.0, 100, "Vegetatif")
    assert result["soil_moisture_available"] is False
    assert "KELEMBAPAN_TANAH" not in result["fuzzy_values"]


def test_fase_tidak_dikenal_ditolak():
    with pytest.raises(ValueError, match="Fase tidak dikenal"):
        hitung_rekomendasi(40, 45, 30, 6.0, 100, "Panen")


def test_status_monitoring_memakai_himpunan_fuzzy_yang_sama():
    status = status_monitoring(10, 27, 60, 4.8)
    assert status == {
        "status_n": "Rendah",
        "status_p": "Sedang",
        "status_k": "Tinggi",
        "status_ph": "Masam",
    }


def test_kelembapan_tanah_memiliki_tiga_status_fuzzy():
    assert derajat_kelembapan(10, DEFAULT)["kering"] == 1.0
    assert derajat_kelembapan(20, DEFAULT)["optimal"] == 1.0
    assert derajat_kelembapan(30, DEFAULT)["basah"] == 1.0
    assert status_monitoring(10, 27, 60, 4.8, 10)["status_kelembapan_tanah"] == "Kering"
    assert status_monitoring(10, 27, 60, 4.8, 20)["status_kelembapan_tanah"] == "Optimal"
    assert status_monitoring(10, 27, 60, 4.8, 30)["status_kelembapan_tanah"] == "Basah"


def test_soil_moisture_menambah_catatan_tanpa_mengubah_z_atau_dosis():
    dry = hitung_rekomendasi(40, 45, 30, 6.0, 100, "Vegetatif", kelembapan_tanah=10)
    optimal = hitung_rekomendasi(40, 45, 30, 6.0, 100, "Vegetatif", kelembapan_tanah=20)
    wet = hitung_rekomendasi(40, 45, 30, 6.0, 100, "Vegetatif", kelembapan_tanah=30)
    assert dry["z"] == optimal["z"] == wet["z"]
    assert dry["doses_g"] == optimal["doses_g"] == wet["doses_g"]
    assert "pastikan tanah cukup lembap" in dry["notes"]
    assert "tunda atau pecahkan dosis" in wet["notes"]
    assert "pastikan tanah cukup lembap" not in optimal["notes"]


@pytest.mark.parametrize("fase", PHASES)
def test_sampel_monitoring_menghasilkan_keluaran_valid_di_lima_fase(fase):
    result = hitung_rekomendasi(23, 6, 33, 6.03, 204.96, fase, kelembapan_tanah=14.88)
    assert result["phase"] == fase
    assert result["soil_moisture_available"] is True
    assert set(result["doses_g"]) == {"urea", "sp36", "kcl", "npk"}
    assert all(math.isfinite(value) and 0 <= value <= 100 for value in result["z"].values())
    assert all(isinstance(value, int) and value >= 0 for value in result["doses_g"].values())
    assert all(0 <= row["alpha"] <= 1 for row in result["active_rules"])
    assert "pastikan tanah cukup lembap" in result["notes"]
    assert "pecahkan dosis (curah hujan tinggi)" in result["notes"]
    assert result["corrections_g"]["dolomit"] is not None
    assert result["corrections_g"]["belerang"] is not None
