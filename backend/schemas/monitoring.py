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
