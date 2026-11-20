import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import text

from auth import get_current_user
from constants import PLANT_VARIETY
from database.session import SessionLocal
from models.rekomendasi_detail import RekomendasiDetail
from models.user import User
from services.recommendation_service import generate_recommendation

router = APIRouter()

BASE_SELECT = """
    SELECT
        r.id, r.monitoring_id, r.fase_id,
        r.jenis_pupuk, r.dosis, r.kategori,
        r.algorithm_version, r.fuzzy_trace,
        r.z_n, r.z_p, r.z_k, r.z_dolomit, r.z_belerang,
        r.created_at,
        m.nitrogen, m.phosphorus, m.potassium, m.ph,
        m.temperature, m.humidity, m.soil_moisture, m.rainfall,
        COALESCE(NULLIF(BTRIM(va.nama_varietas_lama), ''), :varietas) AS varietas,
        CONCAT('Durian ', COALESCE(NULLIF(BTRIM(va.nama_varietas_lama), ''), :varietas)) AS objek_tanaman,
        f.nama AS fase
    FROM rekomendasi r
    JOIN monitoring m ON r.monitoring_id = m.id AND m.user_id = :user_id
    JOIN fase_pertumbuhan f ON r.fase_id = f.id
    LEFT JOIN public.rekomendasi_varietas_archive va ON va.rekomendasi_id = r.id
    WHERE r.user_id = :user_id
"""


def _load_detail_map(db, recommendation_ids):
    if not recommendation_ids:
        return {}
    rows = (
        db.query(RekomendasiDetail)
        .filter(RekomendasiDetail.rekomendasi_id.in_(recommendation_ids))
        .order_by(RekomendasiDetail.id)
        .all()
    )
    grouped = {}
    for row in rows:
        grouped.setdefault(row.rekomendasi_id, []).append({
            "id": row.id,
            "kode_pupuk": row.kode_pupuk,
            "nama_pupuk": row.nama_pupuk,
            "dosis_g": row.dosis_g,
            "dosis_min_g": row.dosis_min_g,
            "dosis_maks_g": row.dosis_maks_g,
            "satuan": row.satuan,
            "kategori": row.kategori,
            "direkomendasikan": bool(row.direkomendasikan),
            "catatan": row.catatan,
        })
    return grouped


def _serialize_rows(db, rows):
    ids = [row["id"] for row in rows]
    detail_map = _load_detail_map(db, ids)
    serialized = []
    for row in rows:
        item = dict(row)
        details = detail_map.get(item["id"], [])
        if not details and item.get("jenis_pupuk"):
            # Kompatibilitas untuk data historis model satu-pupuk.
            details = [{
                "kode_pupuk": "LEGACY",
                "nama_pupuk": item["jenis_pupuk"],
                "dosis_g": None,
                "dosis_min_g": None,
                "dosis_maks_g": None,
                "dosis_kg": item.get("dosis"),
                "satuan": "kg/pohon",
                "kategori": item.get("kategori") or "Rekomendasi lama",
                "direkomendasikan": True,
                "catatan": None,
            }]
        item["items"] = details
        item["profile"] = (item.get("fuzzy_trace") or {}).get("profile")
        item["varietas"] = item.get("varietas") or PLANT_VARIETY
        item["objek_tanaman"] = item.get("objek_tanaman") or f"Durian {PLANT_VARIETY}"
        serialized.append(item)
    return serialized


def _query_recommendations(db, user_id, limit=None):
    query = BASE_SELECT + " ORDER BY r.created_at DESC, r.id DESC"
    params = {"varietas": PLANT_VARIETY, "user_id": user_id}
    if limit is not None:
        query += " LIMIT :limit"
        params["limit"] = limit
    rows = db.execute(text(query), params).mappings().all()
    return _serialize_rows(db, rows)


@router.post("/generate")
def generate(payload: dict, current_user: User = Depends(get_current_user)):
    try:
        monitoring_id = int(payload["monitoring_id"])
        fase_id = int(payload["fase_id"])
    except (KeyError, TypeError, ValueError):
        raise HTTPException(status_code=422, detail="monitoring_id dan fase_id wajib berupa angka")
    return generate_recommendation(
        monitoring_id=monitoring_id,
        fase_id=fase_id,
        user_id=current_user.id,
        profile=payload.get("profile", "A"),
    )


@router.get("/latest")
def latest_recommendation(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        rows = _query_recommendations(db, current_user.id, limit=1)
        return rows[0] if rows else None
    finally:
        db.close()


@router.get("/history")
def recommendation_history(
    limit: int | None = Query(default=None, ge=1, le=500),
    current_user: User = Depends(get_current_user),
):
    db = SessionLocal()
    try:
        return _query_recommendations(db, current_user.id, limit=limit)
    finally:
        db.close()


@router.delete("/{recommendation_id}")
def delete_recommendation(recommendation_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        existing = db.execute(
            text("SELECT id FROM rekomendasi WHERE id = :id AND user_id = :user_id"),
            {"id": recommendation_id, "user_id": current_user.id},
        ).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Data rekomendasi tidak ditemukan.")

        # Rincian dihapus otomatis melalui ON DELETE CASCADE.
        db.execute(
            text("DELETE FROM public.rekomendasi_varietas_archive WHERE rekomendasi_id = :id"),
            {"id": recommendation_id},
        )
        db.execute(
            text("DELETE FROM rekomendasi WHERE id = :id AND user_id = :user_id"),
            {"id": recommendation_id, "user_id": current_user.id},
        )
        db.commit()
        return {"success": True, "message": "Data rekomendasi berhasil dihapus.", "id": recommendation_id}
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.get("/export")
def export_csv(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        records = _query_recommendations(db, current_user.id, limit=None)
        output = io.StringIO(newline="")
        writer = csv.writer(output)
        writer.writerow([
            "Tanggal", "Nitrogen (mg/kg)", "Fosfor (mg/kg)", "Kalium (mg/kg)", "pH",
            "Temperatur (°C)", "Kelembapan udara (%)", "Kelembapan tanah (%)", "Curah hujan (mm)",
            "Objek tanaman", "Fase", "Kode pupuk", "Jenis pupuk", "Dosis", "Satuan",
            "Dosis minimum (g/pohon)", "Dosis maksimum (g/pohon)", "Kategori", "Direkomendasikan", "Catatan",
        ])
        for record in records:
            items = record["items"] or [{
                "kode_pupuk": "-", "nama_pupuk": "Tidak ada rincian", "dosis_g": None,
                "dosis_min_g": None, "dosis_maks_g": None, "kategori": "-", "direkomendasikan": False, "catatan": None,
            }]
            for item in items:
                writer.writerow([
                    record.get("created_at"), record.get("nitrogen"), record.get("phosphorus"),
                    record.get("potassium"), record.get("ph"), record.get("temperature"),
                    record.get("humidity"), record.get("soil_moisture"), record.get("rainfall"), record.get("objek_tanaman"),
                    record.get("fase"), item.get("kode_pupuk"), item.get("nama_pupuk"),
                    (item.get("dosis_g") if item.get("dosis_g") is not None else item.get("dosis_kg")),
                    item.get("satuan"), item.get("dosis_min_g"), item.get("dosis_maks_g"),
                    item.get("kategori"), "Ya" if item.get("direkomendasikan") else "Tidak", item.get("catatan"),
                ])
        output.seek(0)
        filename = "riwayat_rekomendasi_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    finally:
        db.close()
