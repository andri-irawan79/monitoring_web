from sqlalchemy.dialects import postgresql

from database.session import SessionLocal
from models.monitoring import Monitoring
from routes.recommendation import BASE_SELECT
from services.monitoring_query import exclude_scenario_monitoring


def test_monitoring_query_excludes_scenario_sessions_without_excluding_legacy_rows():
    db = SessionLocal()
    try:
        query = exclude_scenario_monitoring(
            db.query(Monitoring).filter(Monitoring.user_id == 123)
        )
        sql = str(
            query.statement.compile(
                dialect=postgresql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        ).upper()

        assert "NOT (EXISTS" in sql
        assert "SIMULATION_SESSIONS.MODE = 'SCENARIO'" in sql
        assert "MONITORING.SIMULATION_SESSION_ID" in sql
    finally:
        db.close()


def test_recommendation_history_query_excludes_scenario_monitoring():
    sql = BASE_SELECT.upper()

    assert "NOT EXISTS" in sql
    assert "SIMULATION_SESSIONS SS" in sql
    assert "SS.MODE = 'SCENARIO'" in sql
    assert "SS.ID = M.SIMULATION_SESSION_ID" in sql
