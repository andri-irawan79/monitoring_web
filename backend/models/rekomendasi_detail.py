from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, String

from database.base import Base


class RekomendasiDetail(Base):
    __tablename__ = "rekomendasi_detail"
    __table_args__ = (Index("ix_rekomendasi_detail_rekomendasi_id", "rekomendasi_id"),)

    id = Column(Integer, primary_key=True)
    rekomendasi_id = Column(
        Integer,
        ForeignKey("rekomendasi.id", ondelete="CASCADE"),
        nullable=False,
    )
    kode_pupuk = Column(String(30), nullable=False)
    nama_pupuk = Column(String(100), nullable=False)
    dosis_g = Column(Integer, nullable=True)
    dosis_min_g = Column(Integer, nullable=True)
    dosis_maks_g = Column(Integer, nullable=True)
    satuan = Column(String(20), nullable=False, default="g/pohon")
    kategori = Column(String(40), nullable=False)
    direkomendasikan = Column(Boolean, nullable=False, default=True)
    catatan = Column(String(255), nullable=True)
