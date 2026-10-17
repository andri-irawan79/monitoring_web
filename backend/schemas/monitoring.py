from pydantic import BaseModel


class MonitoringCreate(BaseModel):

    nitrogen: float
    phosphorus: float
    potassium: float

    temperature: float
    humidity: float

    ph: float
    rainfall: float