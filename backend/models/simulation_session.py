from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from database.base import Base


class SimulationSession(Base):
    __tablename__ = "simulation_sessions"

    id = Column(String(36), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    mode = Column(String(16), nullable=False)  # website | terminal | scenario
    status = Column(
        String(16),
        nullable=False,
        default="starting",
        server_default="starting",
    )  # starting | running | completed | stopped | failed
    target_count = Column(Integer, nullable=False, default=365, server_default="365")
    received_count = Column(Integer, nullable=False, default=0, server_default="0")
    started_at = Column(DateTime, nullable=False, server_default=func.now())
    last_received_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    process_id = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
