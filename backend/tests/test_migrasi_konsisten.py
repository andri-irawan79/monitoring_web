"""Penjaga duplikasi DDL: kolom yang ditambahkan `main.py` saat startup harus sama dengan yang ada di migrasi SQL,
agar dua sumber kebenaran tidak berbeda diam-diam."""
import re
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent
MIGRASI = BACKEND / "migrations"


def _kolom_ditambahkan(sql: str, tabel: str) -> set[str]:
    kolom = set()
    for blok in re.finditer(r"ALTER TABLE\s+(?:public\.)?" + tabel + r"\b(.*?)(?:;|\"\"\"|\"\s*\)\s*\))", sql, re.S | re.I):
        kolom |= {m.group(1).lower() for m in re.finditer(r"ADD COLUMN IF NOT EXISTS\s+(\w+)", blok.group(1), re.I)}
    return kolom


def test_kolom_rekomendasi_main_sama_dengan_migrasi_002():
    main = (BACKEND / "main.py").read_text(encoding="utf-8")
    m002 = (MIGRASI / "002_fis1_fis2_multi_fertilizer.sql").read_text(encoding="utf-8")
    fis = {"algorithm_version", "fuzzy_trace", "z_n", "z_p", "z_k", "z_dolomit", "z_belerang"}
    assert fis <= _kolom_ditambahkan(main, "rekomendasi"), "main.py tidak menambah semua kolom FIS"
    assert fis <= _kolom_ditambahkan(m002, "rekomendasi"), "migrasi 002 tidak menambah semua kolom FIS"


def test_soil_moisture_ada_di_main_dan_migrasi_003():
    main = (BACKEND / "main.py").read_text(encoding="utf-8")
    m003 = (MIGRASI / "003_add_soil_moisture.sql").read_text(encoding="utf-8")
    assert "soil_moisture" in _kolom_ditambahkan(main, "monitoring")
    assert "soil_moisture" in _kolom_ditambahkan(m003, "monitoring")


def test_tabel_arsip_varietas_dibuat_saat_startup_dan_di_skema_dasar():
    """Route riwayat/terbaru/hapus melakukan JOIN ke tabel ini; tanpa pembuatnya instalasi baru error."""
    main = (BACKEND / "main.py").read_text(encoding="utf-8")
    dasar = (MIGRASI / "000_base_schema.sql").read_text(encoding="utf-8")
    assert "CREATE TABLE IF NOT EXISTS public.rekomendasi_varietas_archive" in main
    assert "CREATE TABLE IF NOT EXISTS public.rekomendasi_varietas_archive" in dasar
