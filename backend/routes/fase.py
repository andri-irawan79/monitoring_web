from fastapi import APIRouter, Depends
from sqlalchemy import text

from auth import get_current_user
from database.session import SessionLocal
from models.user import User

router = APIRouter(
    prefix="/fase",
    tags=["Fase"],
)


@router.get("/")
def get_fase(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        result = db.execute(
            text("""
                SELECT id, nama
                FROM public.fase_pertumbuhan
                ORDER BY CASE LOWER(BTRIM(nama))
                    WHEN 'pascapanen' THEN 1
                    WHEN 'vegetatif' THEN 2
                    WHEN 'prapembungaan' THEN 3
                    WHEN 'pembuahan' THEN 4
                    WHEN 'prapanen' THEN 5
                    ELSE 99
                END,
                LOWER(BTRIM(nama)),
                id
            """)
        )
        return [dict(row._mapping) for row in result]
    finally:
        db.close()
