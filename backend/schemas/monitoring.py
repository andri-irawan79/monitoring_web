from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class MonitoringCreate(BaseModel):
    # Rentang validasi pintu masuk (UF-04). Batas atas sengaja longgar terhadap data
    # simulasi (N maks. 140, K maks. 205, curah hujan maks. sekitar 300 mm).
    nitrogen: float = Field(ge=0, le=500, allow_inf_nan=False)
    phosphorus: float = Field(ge=0, le=500, allow_inf_nan=False)
    potassium: float = Field(ge=0, le=500, allow_inf_nan=False)

    temperature: float = Field(ge=-10, le=60, allow_inf_nan=False)
    humidity: float = Field(ge=0, le=100, allow_inf_nan=False)

    ph: float = Field(ge=0, le=14, allow_inf_nan=False)
    soil_moisture: Optional[float] = Field(default=None, ge=0, le=100, allow_inf_nan=False)
    rainfall: float = Field(ge=0, le=2000, allow_inf_nan=False)

    # Tanggal simulasi dikirim oleh simulator.
    # Dibuat opsional agar klien lama tetap kompatibel.
    simulation_date: Optional[date] = None

    # Session fields are optional so older integrations keep working.
    simulation_session_id: Optional[str] = None
    session_record_number: Optional[int] = None
