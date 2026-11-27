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


def test_snapshot_nama_fase_ada_di_model_main_migrasi_dan_skema_dasar():
    main = (BACKEND / "main.py").read_text(encoding="utf-8")
    dasar = (MIGRASI / "000_base_schema.sql").read_text(encoding="utf-8")
    revisi = (MIGRASI / "004_growth_phase_matrix_v1_1.sql").read_text(encoding="utf-8")
    model = (BACKEND / "models" / "rekomendasi.py").read_text(encoding="utf-8")
    assert "fase_nama_snapshot" in main
    assert "fase_nama_snapshot" in dasar
    assert "fase_nama_snapshot" in revisi
    assert "fase_nama_snapshot" in model
    assert "Prapembungaan" in revisi and "Prapanen" in revisi

def test_seed_fase_mempertahankan_pemetaan_id_historis():
    dasar = (MIGRASI / "000_base_schema.sql").read_text(encoding="utf-8")
    pemetaan = (
        "(1, 'Vegetatif'), (2, 'Prapanen'), "
        "(3, 'Prapembungaan'), (4, 'Pascapanen'), (5, 'Pembuahan')"
    )
    assert pemetaan in dasar


def test_migrasi_fase_mengubah_nama_tanpa_mengasumsikan_id():
    revisi = (MIGRASI / "004_growth_phase_matrix_v1_1.sql").read_text(encoding="utf-8")
    assert "WHEN 'panen' THEN 'Prapanen'" in revisi
    assert "WHEN 'pembungaan' THEN 'Prapembungaan'" in revisi
    assert "WHERE LOWER(BTRIM(nama)) IN ('panen', 'pembungaan')" in revisi
    assert "WHERE id = 2" not in revisi
    assert "WHERE id = 3" not in revisi
    assert "fase_nama_snapshot IS NULL" in revisi


def test_endpoint_fase_mengurutkan_berdasarkan_nama_bukan_id():
    route = (BACKEND / "routes" / "fase.py").read_text(encoding="utf-8")
    assert "ORDER BY CASE LOWER(BTRIM(nama))" in route
    urutan = (
        "WHEN 'pascapanen' THEN 1",
        "WHEN 'vegetatif' THEN 2",
        "WHEN 'prapembungaan' THEN 3",
        "WHEN 'pembuahan' THEN 4",
        "WHEN 'prapanen' THEN 5",
    )
    posisi = [route.index(item) for item in urutan]
    assert posisi == sorted(posisi)
    assert "ORDER BY CASE id" not in route
