from pydantic import BaseModel


class RecommendationResponse(BaseModel):

    id: int

    created_at: str

    monitoring_id: int

    varietas: str

    fase: str

    nitrogen: float

    phosphorus: float

    potassium: float

    ph: float

    jenis_pupuk: str

    dosis: float

    kategori: str
    