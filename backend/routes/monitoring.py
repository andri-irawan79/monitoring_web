from fastapi import APIRouter

from database.session import SessionLocal
from models.monitoring import Monitoring
from schemas.monitoring import MonitoringCreate

router = APIRouter()


@router.get("/latest")
def latest_monitoring():
    db = SessionLocal()

    try:
        data = (
            db.query(Monitoring)
            .order_by(Monitoring.id.desc())
            .first()
        )

        if data is None:
            return None

        return {
            "id": data.id,
            "nitrogen": data.nitrogen,
            "phosphorus": data.phosphorus,
            "potassium": data.potassium,
            "temperature": data.temperature,
            "humidity": data.humidity,
            "ph": data.ph,
            "rainfall": data.rainfall,
            "created_at": data.created_at,
            "simulation_date": data.simulation_date,
        }

    finally:
        db.close()


@router.get("/history")
def monitoring_history():
    db = SessionLocal()

    try:
        data = (
            db.query(Monitoring)
            .order_by(Monitoring.id.desc())
            .all()
        )

        return [
            {
                "id": row.id,
                "nitrogen": row.nitrogen,
                "phosphorus": row.phosphorus,
                "potassium": row.potassium,
                "temperature": row.temperature,
                "humidity": row.humidity,
                "ph": row.ph,
                "rainfall": row.rainfall,
                "created_at": row.created_at,
                "simulation_date": row.simulation_date,
            }
            for row in data
        ]

    finally:
        db.close()


@router.post("/")
def create_monitoring(payload: MonitoringCreate):
    db = SessionLocal()

    try:
        data = Monitoring(
            nitrogen=payload.nitrogen,
            phosphorus=payload.phosphorus,
            potassium=payload.potassium,
            temperature=payload.temperature,
            humidity=payload.humidity,
            ph=payload.ph,
            rainfall=payload.rainfall,
            simulation_date=payload.simulation_date,
        )

        db.add(data)
        db.commit()
        db.refresh(data)

        return {
            "message": "Data monitoring berhasil ditambahkan",
            "id": data.id,
            "simulation_date": (
                data.simulation_date.isoformat()
                if data.simulation_date
                else None
            ),
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
