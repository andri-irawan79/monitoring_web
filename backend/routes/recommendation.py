import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import text

from auth import get_current_user
from constants import PLANT_VARIETY
from database.session import SessionLocal
from models.user import User
from services.recommendation_service import generate_recommendation

router = APIRouter()


@router.post("/generate")
def generate(
    payload: dict,
    current_user: User = Depends(get_current_user)
):
    return generate_recommendation(
        monitoring_id=payload["monitoring_id"],
        fase_id=payload["fase_id"],
        user_id=current_user.id
    )


@router.get("/latest")
def latest_recommendation(
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        result = db.execute(
            text("""
                SELECT
                    r.id,
                    r.monitoring_id,
                    r.fase_id,
                    COALESCE(NULLIF(BTRIM(va.nama_varietas_lama), ''), :varietas) AS varietas,
                    CONCAT('Durian ', COALESCE(NULLIF(BTRIM(va.nama_varietas_lama), ''), :varietas)) AS objek_tanaman,
                    f.nama AS fase,
                    r.jenis_pupuk,
                    r.dosis,
                    r.kategori,
                    r.created_at
                FROM rekomendasi r
                JOIN fase_pertumbuhan f ON r.fase_id = f.id
                LEFT JOIN public.rekomendasi_varietas_archive va
                    ON va.rekomendasi_id = r.id
                WHERE r.user_id = :user_id
                ORDER BY r.id DESC
                LIMIT 1
            """),
            {"varietas": PLANT_VARIETY, "user_id": current_user.id}
        )
        row = result.fetchone()
        return dict(row._mapping) if row is not None else None
    finally:
        db.close()


@router.get("/history")
def recommendation_history(
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        result = db.execute(
            text("""
                SELECT
                    r.id,
                    m.nitrogen,
                    m.phosphorus,
                    m.potassium,
                    m.ph,
                    m.temperature,
                    m.humidity,
                    m.rainfall,
                    COALESCE(NULLIF(BTRIM(va.nama_varietas_lama), ''), :varietas) AS varietas,
                    CONCAT('Durian ', COALESCE(NULLIF(BTRIM(va.nama_varietas_lama), ''), :varietas)) AS objek_tanaman,
                    f.nama AS fase,
                    r.jenis_pupuk,
                    r.dosis,
                    r.kategori,
                    r.created_at
                FROM rekomendasi r
                JOIN monitoring m ON r.monitoring_id = m.id
                JOIN fase_pertumbuhan f ON r.fase_id = f.id
                LEFT JOIN public.rekomendasi_varietas_archive va
                    ON va.rekomendasi_id = r.id
                WHERE r.user_id = :user_id
                ORDER BY r.id DESC

            """),
            {"varietas": PLANT_VARIETY, "user_id": current_user.id}
        )
        return [dict(row._mapping) for row in result]
    finally:
        db.close()


@router.delete("/{recommendation_id}")
def delete_recommendation(
    recommendation_id: int,
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        existing = db.execute(
            text(
                "SELECT id FROM rekomendasi "
                "WHERE id = :id AND user_id = :user_id"
            ),
            {"id": recommendation_id, "user_id": current_user.id}
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Data rekomendasi tidak ditemukan."
            )

        # Hapus arsip relasi terlebih dahulu agar tidak melanggar foreign key.
        db.execute(
            text("DELETE FROM public.rekomendasi_varietas_archive WHERE rekomendasi_id = :id"),
            {"id": recommendation_id}
        )
        db.execute(
            text("DELETE FROM rekomendasi WHERE id = :id"),
            {"id": recommendation_id}
        )
        db.commit()
        return {
            "success": True,
            "message": "Data rekomendasi berhasil dihapus.",
            "id": recommendation_id
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.get("/export")
def export_csv(
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        result = db.execute(
            text("""
                SELECT
                    m.nitrogen,
                    m.phosphorus,
                    m.potassium,
                    m.ph,
                    m.temperature,
                    m.humidity,
                    m.rainfall,
                    COALESCE(NULLIF(BTRIM(va.nama_varietas_lama), ''), :varietas) AS varietas,
                    CONCAT('Durian ', COALESCE(NULLIF(BTRIM(va.nama_varietas_lama), ''), :varietas)) AS objek_tanaman,
                    f.nama AS fase,
                    r.jenis_pupuk,
                    r.dosis,
                    r.kategori,
                    r.created_at
                FROM rekomendasi r
                JOIN monitoring m ON r.monitoring_id = m.id
                JOIN fase_pertumbuhan f ON r.fase_id = f.id
                LEFT JOIN public.rekomendasi_varietas_archive va
                    ON va.rekomendasi_id = r.id
                WHERE r.user_id = :user_id
                ORDER BY r.id DESC
            """),
            {"varietas": PLANT_VARIETY, "user_id": current_user.id}
        )

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Tanggal",
            "Nitrogen (ppm)",
            "Fosfor (ppm)",
            "Kalium (ppm)",
            "pH",
            "Temperatur (°C)",
            "Kelembapan (%)",
            "Curah Hujan (mm)",
            "Objek Tanaman",
            "Varietas",
            "Fase",
            "Jenis Pupuk",
            "Dosis (kg/pohon)",
            "Kategori"
        ])

        for row in result:
            row = row._mapping
            writer.writerow([
                row["created_at"],
                row["nitrogen"],
                row["phosphorus"],
                row["potassium"],
                row["ph"],
                row["temperature"],
                row["humidity"],
                row["rainfall"],
                row["objek_tanaman"],
                row["varietas"],
                row["fase"],
                row["jenis_pupuk"],
                row["dosis"],
                row["kategori"]
            ])

        output.seek(0)
        filename = (
            "riwayat_rekomendasi_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".csv"
        )
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    finally:
        db.close()
