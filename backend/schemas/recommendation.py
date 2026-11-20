from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class RecommendationDetailResponse(BaseModel):
    id: Optional[int] = None
    kode_pupuk: str
    nama_pupuk: str
    dosis_g: Optional[int] = None
    dosis_min_g: Optional[int] = None
    dosis_maks_g: Optional[int] = None
    dosis_kg: Optional[float] = None  # only for legacy records
    satuan: str = "g/pohon"
    kategori: str
    direkomendasikan: bool = True
    catatan: Optional[str] = None


class RecommendationResponse(BaseModel):
    id: int
    monitoring_id: int
    fase_id: int
    fase: str
    varietas: str = "Montong"
    objek_tanaman: str = "Durian Montong"
    created_at: datetime
    items: list[RecommendationDetailResponse] = Field(default_factory=list)
    algorithm_version: str = "legacy"
    profile: Optional[str] = None
    fuzzy_trace: dict[str, Any] = Field(default_factory=dict)

    # Nullable legacy columns remain available when reading old recommendations.
    jenis_pupuk: Optional[str] = None
    dosis: Optional[float] = None
    kategori: Optional[str] = None

    # Monitoring context.
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    ph: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    rainfall: Optional[float] = None

    z_n: Optional[float] = None
    z_p: Optional[float] = None
    z_k: Optional[float] = None
    z_dolomit: Optional[float] = None
    z_belerang: Optional[float] = None


class RecommendationGenerateResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    recommendation: Optional[dict[str, Any]] = None
    fuzzy_values: Optional[dict[str, Any]] = None
    fis1: Optional[dict[str, Any]] = None
    fis2: Optional[dict[str, Any]] = None
    active_rules: list[dict[str, Any]] = Field(default_factory=list)
    z_values: dict[str, float] = Field(default_factory=dict)
    target_hara_g: dict[str, float] = Field(default_factory=dict)
    remaining_hara_g: dict[str, float] = Field(default_factory=dict)
    doses_g: dict[str, int] = Field(default_factory=dict)
    corrections_g: dict[str, Any] = Field(default_factory=dict)
    notes: list[str] = Field(default_factory=list)
    parameter_warnings: list[str] = Field(default_factory=list)
