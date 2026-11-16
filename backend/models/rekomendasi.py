from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from database.base import Base


class Rekomendasi(Base):
    __tablename__ = "rekomendasi"

    id = Column(Integer, primary_key=True)
    monitoring_id = Column(Integer, nullable=False)
    fase_id = Column(Integer, nullable=False)
    jenis_pupuk = Column(String, nullable=False)
    dosis = Column(Float, nullable=False)
    kategori = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
