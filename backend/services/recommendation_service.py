from sqlalchemy import text

from database.session import SessionLocal
from models.monitoring import Monitoring
from models.rekomendasi import Rekomendasi
from models.rekomendasi_detail import RekomendasiDetail
from constants import PLANT_VARIETY, PLANT_DISPLAY_NAME
from fuzzy.parameter import get_parameters
from fuzzy.tsukamoto import hitung_rekomendasi


# Nama fase untuk mesin fuzzy dibuat kanonis, tetapi label yang ditampilkan
# tetap diambil dari master fase_pertumbuhan agar sama persis dengan dropdown.
FASE_CANONICAL = {
    "pascapanen": "Pascapanen",
    "vegetatif": "Vegetatif",
    "prapembungaan": "Prapembungaan",
    "pembungaan": "Prapembungaan",  # alias nama master sebelum revisi
    "pembuahan": "Pembuahan",
    "prapanen": "Prapanen",
    "panen": "Prapanen",             # alias nama master sebelum revisi
}


def _normalize_fase_name(value):
    """Normalisasi label master, termasuk variasi 'Pasca Panen'."""
    normalized = "".join(
        character for character in str(value or "").casefold()
        if character.isalnum()
    )
    return FASE_CANONICAL.get(normalized)


def _resolve_fase(db, fase_id):
    """Ambil fase berdasarkan ID master, bukan asumsi urutan ID tetap."""
    try:
        fase_id = int(fase_id)
    except (TypeError, ValueError):
        return None, None, None

    row = db.execute(
        text("SELECT id, nama FROM fase_pertumbuhan WHERE id = :fase_id"),
        {"fase_id": fase_id},
    ).mappings().first()

    if row is None:
        return None, None, None

    fase_display = str(row["nama"] or "").strip()
    fase_canonical = _normalize_fase_name(fase_display)
    if not fase_display or fase_canonical is None:
        return None, None, None

    return int(row["id"]), fase_display, fase_canonical


FERTILIZER_META = {
    "urea": ("UREA", "Urea", "Pupuk hara"),
    "sp36": ("SP36", "SP-36", "Pupuk hara"),
    "kcl": ("KCL", "KCl", "Pupuk hara"),
    "npk": ("NPK161616", "NPK 16-16-16", "Pupuk hara"),
}


def _detail_rows(result):
    rows = []
    for key in ("urea", "sp36", "kcl", "npk"):
        code, name, category = FERTILIZER_META[key]
        dose = int(result["doses_g"][key])
        rows.append({
            "kode_pupuk": code,
            "nama_pupuk": name,
            "dosis_g": dose,
            "dosis_min_g": None,
            "dosis_maks_g": None,
            "satuan": "g/pohon",
            "kategori": category,
            "direkomendasikan": dose > 0,
            "catatan": None if dose > 0 else "Tidak diperlukan berdasarkan hasil perhitungan",
        })

    # FIS-2 bergantung pada pH dan dihitung pada seluruh fase.
    # Rentang koreksi bersifat indikatif dan tidak menggantikan uji tanah.
    corrections = result["corrections_g"]
    for key, code, name in (
        ("dolomit", "DOLOMIT", "Kapur Dolomit"),
        ("belerang", "SULFUR", "Belerang"),
    ):
        dose_range = corrections[key] or [0, 0]
        low, high = int(dose_range[0]), int(dose_range[1])
        rows.append({
            "kode_pupuk": code,
            "nama_pupuk": name,
            "dosis_g": None,
            "dosis_min_g": low,
            "dosis_maks_g": high,
            "satuan": "g/pohon",
            "kategori": "Koreksi pH",
            "direkomendasikan": high > 0,
            "catatan": (
                "Rentang dosis indikatif; verifikasi analisis tanah dan kebutuhan kapur/belerang sebelum aplikasi"
                if high > 0 else
                "Tidak diperlukan berdasarkan hasil perhitungan pH"
            ),
        })
    return rows


def generate_recommendation(monitoring_id, fase_id, user_id, profile="A"):
    """Hitung FIS-1 + FIS-2 dengan fase dari master database."""
    db = SessionLocal()
    try:
        monitoring = (
            db.query(Monitoring)
            .filter(
                Monitoring.id == monitoring_id,
                Monitoring.user_id == user_id,
            )
            .first()
        )
        if not monitoring:
            return {"success": False, "message": "Data monitoring tidak ditemukan"}

        resolved_fase_id, fase_display, fase_nama = _resolve_fase(db, fase_id)
        if not fase_nama:
            return {
                "success": False,
                "message": "Fase pertumbuhan tidak valid atau tidak terdaftar pada master fase.",
            }

        try:
            par = get_parameters(profile)
            calculation = hitung_rekomendasi(
                n=float(monitoring.nitrogen),
                p=float(monitoring.phosphorus),
                k=float(monitoring.potassium),
                ph=float(monitoring.ph),
                hujan=float(monitoring.rainfall or 0),
                fase=fase_nama,
                par=par,
                # Gunakan kelembapan tanah bila tersedia; jangan gunakan humidity
                # karena humidity adalah kelembapan udara.
                kelembapan_tanah=(
                    float(monitoring.soil_moisture)
                    if monitoring.soil_moisture is not None
                    else None
                ),
            )
        except (TypeError, ValueError) as error:
            return {"success": False, "message": str(error)}

        calculation["monitoring_context"] = {
            "temperature": float(monitoring.temperature) if monitoring.temperature is not None else None,
            "air_humidity": float(monitoring.humidity) if monitoring.humidity is not None else None,
            "soil_moisture": float(monitoring.soil_moisture) if monitoring.soil_moisture is not None else None,
            "rainfall_mm": float(monitoring.rainfall) if monitoring.rainfall is not None else None,
            "air_humidity_used_as_soil_moisture": False,
        }

        z = calculation["z"]
        recommendation = Rekomendasi(
            user_id=user_id,
            monitoring_id=monitoring_id,
            fase_id=resolved_fase_id,
            fase_nama_snapshot=fase_display,
            # Field lama dibuat NULL untuk header yang berisi beberapa produk.
            jenis_pupuk=None,
            dosis=None,
            kategori=None,
            algorithm_version="FIS1-FIS2-phase-v1.1",
            fuzzy_trace=calculation,
            z_n=z["n"],
            z_p=z["p"],
            z_k=z["k"],
            z_dolomit=z["dolomit"],
            z_belerang=z["belerang"],
        )
        db.add(recommendation)
        db.flush()

        detail_payloads = _detail_rows(calculation)
        for item in detail_payloads:
            db.add(RekomendasiDetail(rekomendasi_id=recommendation.id, **item))

        db.commit()
        db.refresh(recommendation)

        return {
            "success": True,
            "recommendation": {
                "id": recommendation.id,
                "varietas": PLANT_VARIETY,
                "objek_tanaman": PLANT_DISPLAY_NAME,
                # Gunakan label master yang sama dengan opsi dropdown.
                "fase": fase_display,
                "created_at": recommendation.created_at,
                "algorithm_version": recommendation.algorithm_version,
                "profile": calculation["profile"],
                "items": detail_payloads,
                "notes": calculation["notes"],
                "parameter_warnings": calculation["parameter_warnings"],
            },
            "fuzzy_values": calculation["fuzzy_values"],
            "fis1": calculation["fis1"],
            "fis2": calculation["fis2"],
            "active_rules": calculation["active_rules"],
            "z_values": calculation["z"],
            "target_hara_g": calculation["target_hara_g"],
            "remaining_hara_g": calculation["remaining_hara_g"],
            "doses_g": calculation["doses_g"],
            "corrections_g": calculation["corrections_g"],
            "notes": calculation["notes"],
            "parameter_warnings": calculation["parameter_warnings"],
            "monitoring_context": calculation["monitoring_context"],
        }
    except Exception as error:
        db.rollback()
        return {"success": False, "message": str(error)}
    finally:
        db.close()
