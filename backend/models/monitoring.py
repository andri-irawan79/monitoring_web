from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy import Date

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
    rainfall = Column(Float)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )
    simulation_date = Column(Date)