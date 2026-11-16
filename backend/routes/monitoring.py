import os

from fastapi import APIRouter, Depends
from auth import get_current_user, verify_simulator_key
from models.user import User
from sqlalchemy import func

from database.session import SessionLocal
from models.monitoring import Monitoring
from schemas.monitoring import MonitoringCreate

router = APIRouter()

SIMULATOR_STATUS_TIMEOUT_SECONDS = float(
    os.getenv("SIMULATOR_STATUS_TIMEOUT_SECONDS", "8")
)


@router.get("/latest")
def latest_monitoring(current_user: User = Depends(get_current_user)):
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
def monitoring_history(current_user: User = Depends(get_current_user)):
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


@router.get("/simulator-status")
def simulator_status(current_user: User = Depends(get_current_user)):
    """Report whether a simulator delivery was recently committed."""
    db = SessionLocal()

    try:
        latest = (
            db.query(
                Monitoring.created_at,
                func.extract(
                    "epoch",
                    func.now() - Monitoring.created_at
                ).label("age_seconds"),
            )
            .order_by(Monitoring.id.desc())
            .first()
        )

        last_received_at = latest[0] if latest else None
        age_seconds = (
            max(0.0, float(latest[1]))
            if latest and latest[1] is not None
            else None
        )
        active = (
            age_seconds is not None
            and age_seconds <= SIMULATOR_STATUS_TIMEOUT_SECONDS
        )

        return {
            "active": active,
            "last_received_at": (
                last_received_at.isoformat()
                if last_received_at
                else None
            ),
            "seconds_since_last_received": (
                round(age_seconds, 1)
                if age_seconds is not None
                else None
            ),
            "timeout_seconds": SIMULATOR_STATUS_TIMEOUT_SECONDS,
        }

    finally:
        db.close()


@router.post("/")
def create_monitoring(
    payload: MonitoringCreate,
    simulator_authorized: bool = Depends(verify_simulator_key)
):
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
