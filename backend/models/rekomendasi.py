from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from database.base import Base


class Rekomendasi(Base):

    __tablename__ = "rekomendasi"

    id = Column(Integer, primary_key=True)

    monitoring_id = Column(Integer)

    varietas_id = Column(Integer)

    fase_id = Column(Integer)

    jenis_pupuk = Column(String)

    dosis = Column(Float)

    kategori = Column(String)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )