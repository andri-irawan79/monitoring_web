from datetime import date
from typing import Optional

from pydantic import BaseModel


class MonitoringCreate(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float

    temperature: float
    humidity: float

    ph: float
    rainfall: float

    # Tanggal simulasi dikirim oleh simulator.
    # Dibuat opsional agar klien lama tetap kompatibel.
    simulation_date: Optional[date] = None

    # Session fields are optional so older integrations keep working.
    simulation_session_id: Optional[str] = None
    session_record_number: Optional[int] = None
