import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import text

from auth import get_current_user
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
        fase_id=payload["fase_id"]
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
                    r.varietas_id,
                    r.fase_id,
                    v.nama AS varietas,
                    f.nama AS fase,
                    r.jenis_pupuk,
                    r.dosis,
                    r.kategori,
                    r.created_at
                FROM rekomendasi r
                JOIN varietas v ON r.varietas_id = v.id
                JOIN fase_pertumbuhan f ON r.fase_id = f.id
                ORDER BY r.id DESC
                LIMIT 1
            """)
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
                    v.nama AS varietas,
                    f.nama AS fase,
                    r.jenis_pupuk,
                    r.dosis,
                    r.kategori,
                    r.created_at
                FROM rekomendasi r
                JOIN monitoring m ON r.monitoring_id = m.id
                JOIN varietas v ON r.varietas_id = v.id
                JOIN fase_pertumbuhan f ON r.fase_id = f.id
                ORDER BY r.id DESC
                LIMIT 10
            """)
        )
        return [dict(row._mapping) for row in result]
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
                    v.nama AS varietas,
                    f.nama AS fase,
                    r.jenis_pupuk,
                    r.dosis,
                    r.kategori,
                    r.created_at
                FROM rekomendasi r
                JOIN monitoring m ON r.monitoring_id = m.id
                JOIN varietas v ON r.varietas_id = v.id
                JOIN fase_pertumbuhan f ON r.fase_id = f.id
                ORDER BY r.id DESC
            """)
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
