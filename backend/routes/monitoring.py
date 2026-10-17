from fastapi import APIRouter

from database.session import SessionLocal
from models.monitoring import Monitoring
from schemas.monitoring import MonitoringCreate

router = APIRouter()


# Endpoint 1
@router.get("/latest")
def latest_monitoring():

    db = SessionLocal()

    data = (
        db.query(Monitoring)
        .order_by(Monitoring.id.desc())
        .first()
    )

    db.close()

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


# Endpoint 2
@router.get("/history")
def monitoring_history():

    db = SessionLocal()

    data = (
        db.query(Monitoring)
        .order_by(Monitoring.id.desc())
        .all()
    )

    db.close()

    result = []

    for row in data:
        result.append({
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
        })

    return result


@router.post("/")
def create_monitoring(payload: MonitoringCreate):

    db = SessionLocal()

    data = Monitoring(

        nitrogen=payload.nitrogen,
        phosphorus=payload.phosphorus,
        potassium=payload.potassium,

        temperature=payload.temperature,
        humidity=payload.humidity,

        ph=payload.ph,
        rainfall=payload.rainfall
    )

    db.add(data)

    db.commit()

    db.refresh(data)

    db.close()

    return {
        "message": "Data monitoring berhasil ditambahkan",
        "id": data.id
    }