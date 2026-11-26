"""Validasi pintu masuk data monitoring (UF-04): nilai di luar rentang ditolak sebelum disimpan."""
import pytest

pydantic = pytest.importorskip("pydantic")

from schemas.monitoring import MonitoringCreate  # noqa: E402

VALID = {"nitrogen": 40, "phosphorus": 45, "potassium": 30, "temperature": 27.5, "humidity": 90, "ph": 6.0,
         "rainfall": 100, "soil_moisture": 20}


def _buat(**ubah):
    return MonitoringCreate(**{**VALID, **ubah})


def test_data_valid_diterima():
    assert _buat().ph == 6.0


@pytest.mark.parametrize("ubah", [
    {"ph": 15}, {"ph": -1}, {"nitrogen": -5}, {"phosphorus": -1}, {"potassium": 501}, {"humidity": 101},
    {"temperature": 61}, {"temperature": -11}, {"rainfall": -1}, {"rainfall": 2001}, {"soil_moisture": 150},
])
def test_nilai_di_luar_rentang_ditolak(ubah):
    with pytest.raises(pydantic.ValidationError):
        _buat(**ubah)


def test_nilai_kosong_atau_bukan_angka_ditolak():
    with pytest.raises(pydantic.ValidationError):
        MonitoringCreate(**{**VALID, "phosphorus": None})
    with pytest.raises(pydantic.ValidationError):
        MonitoringCreate(**{**VALID, "nitrogen": "abc"})
    with pytest.raises(pydantic.ValidationError):
        MonitoringCreate(**{**VALID, "ph": float("nan")})
