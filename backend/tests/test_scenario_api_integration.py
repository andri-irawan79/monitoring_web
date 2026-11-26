from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models.monitoring import Monitoring
from models.simulation_session import SimulationSession
from models.user import User
from routes import monitoring as monitoring_routes
from simulator import simulator


REPO_ROOT = Path(__file__).resolve().parents[2]
SCENARIO_FILE = REPO_ROOT / "riset" / "skenario_uji.csv"


def test_fastapi_accepts_51_valid_and_rejects_4_invalid_without_polluting_history(
    monkeypatch,
):
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
            full_name="Scenario Test",
            email="scenario-test@example.invalid",
            password_hash="not-used",
            auth_version=0,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    monkeypatch.setattr(monitoring_routes, "SessionLocal", TestSessionLocal)

    app = FastAPI()
    app.include_router(monitoring_routes.router, prefix="/monitoring")
    app.dependency_overrides[monitoring_routes.get_current_user] = lambda: user
    app.dependency_overrides[monitoring_routes.verify_simulator_key] = lambda: True

    try:
        with TestClient(app) as client:
            start = client.post("/monitoring/sessions/scenario/start")
            assert start.status_code == 200
            session = start.json()["session"]
            session_id = session["id"]
            assert session["mode"] == "scenario"
            assert session["target_count"] == 51
            assert session["received_count"] == 0

            dataframe = simulator.load_scenarios(SCENARIO_FILE)
            valid_record_number = 0
            valid_count = 0
            invalid_count = 0

            for scenario_index, (_, row) in enumerate(dataframe.iterrows()):
                is_valid = str(row["jenis"]).strip() == "valid"
                if is_valid:
                    valid_record_number += 1

                payload = simulator.build_scenario_payload(
                    row,
                    session_id=session_id if is_valid else None,
                    session_record_number=valid_record_number if is_valid else None,
                    scenario_index=scenario_index,
                )
                response = client.post("/monitoring/", json=payload)

                if is_valid:
                    assert response.status_code == 200, (
                        row["id"], response.status_code, response.text
                    )
                    assert response.json()["id"] is not None
                    valid_count += 1
                else:
                    assert response.status_code == 422, (
                        row["id"], response.status_code, response.text
                    )
                    fields = simulator._validation_error_fields(response.json())
                    assert simulator.SCENARIO_INVALID_FIELDS[str(row["id"])] in fields
                    invalid_count += 1

            assert valid_count == 51
            assert invalid_count == 4

            with TestSessionLocal() as db:
                saved = db.query(Monitoring).all()
                saved_session = (
                    db.query(SimulationSession)
                    .filter(SimulationSession.id == session_id)
                    .one()
                )
                assert len(saved) == 51
                assert saved_session.received_count == 51
                assert saved_session.target_count == 51
                assert saved_session.status == "completed"
                assert all(row.simulation_session_id == session_id for row in saved)

            # Scenario sessions and their records are deliberately invisible to
            # normal monitoring/history and the frontend's session-status poll.
            assert client.get("/monitoring/latest").json() is None
            assert client.get("/monitoring/history").json() == []
            assert client.get("/monitoring/sessions/status").json()["session"] is None

            # A normal terminal session remains usable and visible after the
            # scenario-only session has completed.
            normal_start = client.post("/monitoring/sessions/terminal/start")
            assert normal_start.status_code == 200
            normal_session_id = normal_start.json()["session"]["id"]
            normal_row = dataframe.loc[dataframe["id"] == "SK-01"].iloc[0]
            normal_payload = simulator.build_scenario_payload(
                normal_row,
                session_id=normal_session_id,
                session_record_number=1,
            )
            normal_response = client.post("/monitoring/", json=normal_payload)
            assert normal_response.status_code == 200

            history = client.get("/monitoring/history")
            assert history.status_code == 200
            assert len(history.json()) == 1
            assert history.json()[0]["id"] == normal_response.json()["id"]
            assert client.get("/monitoring/latest").json()["id"] == normal_response.json()["id"]
            assert (
                client.get("/monitoring/sessions/status").json()["session"]["mode"]
                == "terminal"
            )
    finally:
        engine.dispose()
