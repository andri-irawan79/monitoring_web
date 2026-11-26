from sqlalchemy import func

from database.session import SessionLocal
from models.monitoring import Monitoring
from models.rekomendasi import Rekomendasi
from services.monitoring_query import exclude_scenario_monitoring


def get_dashboard_summary(user_id: int):
    db = SessionLocal()

    try:
        normal_monitoring = exclude_scenario_monitoring(
            db.query(Monitoring).filter(Monitoring.user_id == user_id)
        )

        total_monitoring = normal_monitoring.count()

        normal_recommendations = exclude_scenario_monitoring(
            db.query(Rekomendasi)
            .join(Monitoring, Monitoring.id == Rekomendasi.monitoring_id)
            .filter(
                Rekomendasi.user_id == user_id,
                Monitoring.user_id == user_id,
            )
        )
        total_recommendation = normal_recommendations.count()

        avg = normal_monitoring.with_entities(
            func.avg(Monitoring.nitrogen),
            func.avg(Monitoring.phosphorus),
            func.avg(Monitoring.potassium),
            func.avg(Monitoring.ph),
        ).first()

        return {
            "success": True,
            "summary": {
                "total_monitoring": total_monitoring,
                "total_recommendation": total_recommendation,
                "avg_nitrogen": round(avg[0] or 0, 2),
                "avg_phosphorus": round(avg[1] or 0, 2),
                "avg_potassium": round(avg[2] or 0, 2),
                "avg_ph": round(avg[3] or 0, 2),
            },
        }

    finally:
        db.close()
