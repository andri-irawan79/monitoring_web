import sys
from pathlib import Path

import pytest

from simulator import simulator


REPO_ROOT = Path(__file__).resolve().parents[2]
SCENARIO_FILE = REPO_ROOT / "riset" / "skenario_uji.csv"


def test_scenario_csv_has_51_valid_and_4_invalid_rows():
    dataframe = simulator.load_scenarios(SCENARIO_FILE)

    assert len(dataframe) == 55
    assert int((dataframe["jenis"] == "valid").sum()) == 51
    assert int((dataframe["jenis"] == "tidak_valid").sum()) == 4


def test_invalid_blank_phosphorus_is_sent_as_json_null_without_session_metadata():
    dataframe = simulator.load_scenarios(SCENARIO_FILE)
    row = dataframe.loc[dataframe["id"] == "SK-55"].iloc[0]

    payload = simulator.build_scenario_payload(row)

    assert payload["phosphorus"] is None
    assert "simulation_session_id" not in payload
    assert "session_record_number" not in payload


def test_valid_scenario_requires_and_receives_session_metadata():
    dataframe = simulator.load_scenarios(SCENARIO_FILE)
    row = dataframe.loc[dataframe["id"] == "SK-01"].iloc[0]

    with pytest.raises(ValueError):
        simulator.build_scenario_payload(row)

    payload = simulator.build_scenario_payload(
        row,
        session_id="scenario-session",
        session_record_number=1,
    )
    assert payload["simulation_session_id"] == "scenario-session"
    assert payload["session_record_number"] == 1
    assert payload["nitrogen"] == 0


def test_scenario_runner_checks_all_55_results_and_counts_only_51_valid(monkeypatch):
    sent_payloads = []
    finished = []
    received = 0

    monkeypatch.setattr(simulator, "authenticate_terminal_user", lambda: "test-token")
    monkeypatch.setattr(
        simulator, "create_scenario_session", lambda token: "scenario-session"
    )
    monkeypatch.setattr(simulator, "finish_session", lambda *args: finished.append(args))
    monkeypatch.setattr(simulator.time, "sleep", lambda _seconds: None)

    def fake_send_record(payload, accept_validation_error=False):
        nonlocal received
        sent_payloads.append(payload)
        if "simulation_session_id" in payload:
            assert accept_validation_error is False
            received += 1
            return {
                "status_code": 200,
                "body": {
                    "id": received,
                    "session_received_count": received,
                    "session_target_count": 51,
                },
            }

        assert accept_validation_error is True
        if payload["nitrogen"] is not None and payload["nitrogen"] < 0:
            field = "nitrogen"
        elif payload["ph"] is not None and payload["ph"] > 14:
            field = "ph"
        elif payload["soil_moisture"] is not None and payload["soil_moisture"] > 100:
            field = "soil_moisture"
        elif payload["phosphorus"] is None:
            field = "phosphorus"
        else:
            field = "unexpected"
        return {
            "status_code": 422,
            "body": {"detail": [{"loc": ["body", field], "msg": "invalid"}]},
        }

    monkeypatch.setattr(simulator, "send_record", fake_send_record)

    assert simulator.run_scenario_mode(SCENARIO_FILE, interval_seconds=0) is True
    assert len(sent_payloads) == 55
    assert received == 51
    assert [p["session_record_number"] for p in sent_payloads if "session_record_number" in p] == list(range(1, 52))
    assert all(
        "simulation_session_id" not in p and "session_record_number" not in p
        for p in sent_payloads
        if "simulation_session_id" not in p
    )
    assert finished[-1][0] == "scenario-session"
    assert finished[-1][1] == "completed"


def test_scenario_runner_fails_when_422_reports_the_wrong_field(monkeypatch):
    monkeypatch.setattr(simulator, "authenticate_terminal_user", lambda: "test-token")
    monkeypatch.setattr(
        simulator, "create_scenario_session", lambda token: "scenario-session"
    )
    finished = []
    monkeypatch.setattr(simulator, "finish_session", lambda *args: finished.append(args))
    monkeypatch.setattr(simulator.time, "sleep", lambda _seconds: None)

    def fake_send_record(payload, accept_validation_error=False):
        if "simulation_session_id" in payload:
            return {
                "status_code": 200,
                "body": {
                    "id": payload["session_record_number"],
                    "session_received_count": payload["session_record_number"],
                    "session_target_count": 51,
                },
            }
        return {
            "status_code": 422,
            "body": {"detail": [{"loc": ["body", "wrong_field"], "msg": "invalid"}]},
        }

    monkeypatch.setattr(simulator, "send_record", fake_send_record)

    assert simulator.run_scenario_mode(SCENARIO_FILE, interval_seconds=0) is False
    assert finished[-1][1] == "failed"


def test_normal_simulation_still_posts_365_ordered_records(monkeypatch):
    sent_payloads = []
    finished = []

    monkeypatch.setattr(
        sys,
        "argv",
        ["simulator.py", "--session-id", "normal-session", "--interval", "0"],
    )
    monkeypatch.setattr(simulator, "finish_session", lambda *args: finished.append(args))
    monkeypatch.setattr(simulator.time, "sleep", lambda _seconds: None)

    def fake_send_record(payload):
        sent_payloads.append(payload)
        return {
            "status_code": 200,
            "body": {
                "id": len(sent_payloads),
                "session_received_count": len(sent_payloads),
                "session_target_count": 365,
                "duplicate": False,
            },
        }

    monkeypatch.setattr(simulator, "send_record", fake_send_record)

    simulator.main()

    assert len(sent_payloads) == 365
    assert [p["session_record_number"] for p in sent_payloads] == list(range(1, 366))
    assert all(p["simulation_session_id"] == "normal-session" for p in sent_payloads)
    assert finished[-1][1] == "completed"
