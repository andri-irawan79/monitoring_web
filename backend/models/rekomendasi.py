from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from database.base import Base


class Rekomendasi(Base):
    """Header rekomendasi; rincian jenis pupuk disimpan di rekomendasi_detail."""

    __tablename__ = "rekomendasi"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    monitoring_id = Column(Integer, nullable=False)
    fase_id = Column(Integer, nullable=False)

    # Kolom lama dipertahankan untuk membaca riwayat rekomendasi satu-pupuk.
    jenis_pupuk = Column(String, nullable=True)
    dosis = Column(Float, nullable=True)
    kategori = Column(String, nullable=True)

    algorithm_version = Column(String(40), nullable=False, default="legacy", server_default="legacy")
    fuzzy_trace = Column(JSONB, nullable=False, default=dict)
    z_n = Column(Float, nullable=True)
    z_p = Column(Float, nullable=True)
    z_k = Column(Float, nullable=True)
    z_dolomit = Column(Float, nullable=True)
    z_belerang = Column(Float, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
