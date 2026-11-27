from fastapi import APIRouter, Depends
from auth import get_current_user
from models.user import User
from sqlalchemy import text

from database.session import SessionLocal

router = APIRouter(
    prefix="/fase",
    tags=["Fase"]
)


@router.get("/")
def get_fase(current_user: User = Depends(get_current_user)):

    db = SessionLocal()

    try:

        result = db.execute(
            text("""
                SELECT id,nama
                FROM fase_pertumbuhan
                ORDER BY CASE id
                    WHEN 5 THEN 1  -- Pascapanen
                    WHEN 1 THEN 2  -- Vegetatif
                    WHEN 2 THEN 3  -- Prapembungaan
                    WHEN 3 THEN 4  -- Pembuahan
                    WHEN 4 THEN 5  -- Prapanen
                    ELSE 99
                END, id
            """)
        )

        return [
            dict(row._mapping)
            for row in result
        ]

    finally:
        db.close()