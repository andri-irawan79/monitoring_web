from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from database.base import Base


class Monitoring(Base):
    __tablename__ = "monitoring"

    id = Column(Integer, primary_key=True)

    nitrogen = Column(Float)
    phosphorus = Column(Float)
    potassium = Column(Float)

    temperature = Column(Float)
    humidity = Column(Float)

    ph = Column(Float)
    soil_moisture = Column(Float, nullable=True)
    rainfall = Column(Float)

    created_at = Column(DateTime, server_default=func.now())
    simulation_date = Column(Date)

    # Nullable for pre-existing rows; new simulator records always have an owner.
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    simulation_session_id = Column(String(36), nullable=True)
    session_record_number = Column(Integer, nullable=True)
