"""Query helper to keep scenario-validation records out of normal views."""

from sqlalchemy import exists

from models.monitoring import Monitoring
from models.simulation_session import SimulationSession


def exclude_scenario_monitoring(query):
    """Exclude monitoring rows linked to a scenario-only simulation session.

    The NOT EXISTS condition intentionally preserves legacy rows whose
    simulation_session_id is NULL.
    """
    is_scenario_record = exists().where(
        SimulationSession.id == Monitoring.simulation_session_id,
        SimulationSession.mode == "scenario",
    )
    return query.filter(~is_scenario_record)
