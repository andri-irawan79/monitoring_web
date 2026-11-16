from fastapi import FastAPI
from database.connection import engine
from models.user import User
from routes.auth import router as auth_router
from routes.monitoring import router as monitoring_router
from routes.varietas import router as varietas_router
from routes.fase import router as fase_router
from routes.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware
from routes.recommendation import (
    router as recommendation_router
)

app = FastAPI(title="Durian Monitoring API")


@app.on_event("startup")
def create_auth_table():
    # Membuat tabel akun apabila belum tersedia tanpa mengubah tabel lama.
    User.__table__.create(bind=engine, checkfirst=True)

app.include_router(auth_router)

app.include_router(
    monitoring_router,
    prefix="/monitoring",
    tags=["Monitoring"]
)

app.include_router(
    recommendation_router,
    prefix="/recommendation"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(varietas_router)
app.include_router(fase_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "message": "Durian Monitoring API"
    }