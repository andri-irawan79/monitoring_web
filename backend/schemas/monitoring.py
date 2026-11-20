from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class MonitoringCreate(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float

    temperature: float
    humidity: float

    ph: float
    soil_moisture: Optional[float] = Field(default=None, ge=0, le=100)
    rainfall: float

    # Tanggal simulasi dikirim oleh simulator.
    # Dibuat opsional agar klien lama tetap kompatibel.
    simulation_date: Optional[date] = None

    # Session fields are optional so older integrations keep working.
    simulation_session_id: Optional[str] = None
    session_record_number: Optional[int] = None
