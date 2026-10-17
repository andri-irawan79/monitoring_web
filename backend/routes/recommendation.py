import csv
import io
from datetime import datetime

from fastapi.responses import StreamingResponse
from fastapi import APIRouter
from database.session import SessionLocal
from models.rekomendasi import Rekomendasi
from sqlalchemy import text

from services.recommendation_service import (
    generate_recommendation
)

router = APIRouter()


@router.post("/generate")
def generate(payload: dict):

    return generate_recommendation(

        monitoring_id=
            payload["monitoring_id"],

        varietas_id=
            payload["varietas_id"],

        fase_id=
            payload["fase_id"]
    )

# @router.get("/latest")
# def latest_recommendation():

#     db = SessionLocal()

#     data = (
#         db.query(Rekomendasi)
#         .order_by(
#             Rekomendasi.id.desc()
#         )
#         .first()
#     )

#     db.close()

#     return data

# @router.get("/history")
# def recommendation_history():

    db = SessionLocal()

    data = (
        db.query(Rekomendasi)
        .order_by(
            Rekomendasi.id.desc()
        )
        .all()
    )

    result = []

    for row in data:

        result.append({

            "id": row.id,

            "monitoring_id":
                row.monitoring_id,

            "varietas_id":
                row.varietas_id,

            "fase_id":
                row.fase_id,

            "jenis_pupuk":
                row.jenis_pupuk,

            "dosis":
                row.dosis,

            "kategori":
                row.kategori,

            "created_at":
                row.created_at
        })

    db.close()

    return result   

@router.get("/latest")
def latest_recommendation():

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

                JOIN varietas v
                    ON r.varietas_id=v.id

                JOIN fase_pertumbuhan f
                    ON r.fase_id=f.id

                ORDER BY r.id DESC

                LIMIT 1

            """)
        )

        row = result.fetchone()

        if row is None:

            return None

        return dict(row._mapping)

    finally:

        db.close()

@router.get("/history")
def recommendation_history():

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

                        JOIN monitoring m
                        ON r.monitoring_id = m.id

                        JOIN varietas v
                        ON r.varietas_id = v.id

                        JOIN fase_pertumbuhan f
                        ON r.fase_id = f.id

                        ORDER BY r.id DESC
                 
                        LIMIT 10;

            """)
        )

        return [

            dict(row._mapping)

            for row in result

        ]

    finally:

        db.close()


@router.get("/export")
def export_csv():

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

                JOIN monitoring m
                    ON r.monitoring_id = m.id

                JOIN varietas v
                    ON r.varietas_id = v.id

                JOIN fase_pertumbuhan f
                    ON r.fase_id = f.id

                ORDER BY r.id DESC

            """)
        )

        output = io.StringIO()

        writer = csv.writer(output)

        writer.writerow([
            "Tanggal",
            "Nitrogen (mg/kg)",
            "Fosfor (mg/kg)",
            "Kalium (mg/kg)",
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
                "Content-Disposition":
                f"attachment; filename={filename}"
            }

        )

    finally:

        db.close()