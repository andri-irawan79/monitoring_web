from sqlalchemy import func

from database.session import SessionLocal

from models.monitoring import Monitoring
from models.rekomendasi import Rekomendasi


def get_dashboard_summary(user_id: int):

    db = SessionLocal()

    try:

        total_monitoring = (
            db.query(Monitoring)
            .filter(Monitoring.user_id == user_id)
            .count()
        )

        total_recommendation = (
            db.query(Rekomendasi)
            .filter(Rekomendasi.user_id == user_id)
            .count()
        )

        avg = db.query(
            func.avg(Monitoring.nitrogen),
            func.avg(Monitoring.phosphorus),
            func.avg(Monitoring.potassium),
            func.avg(Monitoring.ph)
        ).filter(
            Monitoring.user_id == user_id
        ).first()

        return {
            "success": True,
            "summary": {
                "total_monitoring": total_monitoring,
                "total_recommendation": total_recommendation,
                "avg_nitrogen": round(avg[0] or 0, 2),
                "avg_phosphorus": round(avg[1] or 0, 2),
                "avg_potassium": round(avg[2] or 0, 2),
                "avg_ph": round(avg[3] or 0, 2)
            }
        }

    finally:
        db.close()
