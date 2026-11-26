from datetime import date, datetime

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models.monitoring import Monitoring
from models.simulation_session import SimulationSession
from models.user import User
from routes import monitoring as monitoring_routes


def test_latest_and_history_follow_received_timestamp_not_dataset_date(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    User.__table__.create(bind=engine)
    SimulationSession.__table__.create(bind=engine)
    Monitoring.__table__.create(bind=engine)
    TestSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

    with TestSessionLocal() as db:
        user = User(
            id=1,
            full_name="History Order Test",
            email="history-order@example.invalid",
            password_hash="not-used",
            auth_version=0,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.add_all(
            [
                Monitoring(
                    id=1,
                    nitrogen=23,
                    phosphorus=6,
                    potassium=33,
                    temperature=29.18,
                    humidity=92.73,
                    ph=6.03,
                    soil_moisture=14.88,
                    rainfall=204.96,
                    simulation_date=date(2026, 1, 3),
                    created_at=datetime(2026, 11, 27, 6, 25, 0),
                    user_id=1,
                ),
                Monitoring(
                    id=2,
                    nitrogen=111,
                    phosphorus=87,
                    potassium=48,
                    temperature=26.40,
                    humidity=81.36,
                    ph=5.57,
                    soil_moisture=13.12,
                    rainfall=98.17,
                    simulation_date=date(2026, 1, 1),
                    created_at=datetime(2026, 11, 27, 6, 20, 0),
                    user_id=1,
                ),
                Monitoring(
                    id=3,
                    nitrogen=13,
                    phosphorus=5,
                    potassium=8,
                    temperature=23.85,
                    humidity=90.11,
                    ph=7.47,
                    soil_moisture=14.46,
                    rainfall=103.92,
                    simulation_date=date(2026, 12, 31),
                    created_at=datetime(2026, 11, 26, 12, 0, 0),
                    user_id=1,
                ),
            ]
        )
        db.commit()
        db.refresh(user)

    monkeypatch.setattr(monitoring_routes, "SessionLocal", TestSessionLocal)
    app = FastAPI()
    app.include_router(monitoring_routes.router, prefix="/monitoring")
    app.dependency_overrides[monitoring_routes.get_current_user] = lambda: user

    try:
        with TestClient(app) as client:
            history = client.get("/monitoring/history")
            assert history.status_code == 200
            assert [row["id"] for row in history.json()] == [1, 2, 3]
            assert [row["simulation_date"] for row in history.json()] == [
                "2026-01-03",
                "2026-01-01",
                "2026-12-31",
            ]

            latest = client.get("/monitoring/latest")
            assert latest.status_code == 200
            assert latest.json()["id"] == 1
    finally:
        engine.dispose()
