from fastapi import APIRouter, Depends
from auth import get_current_user
from models.user import User
from sqlalchemy import text

from database.session import SessionLocal

router = APIRouter(
    prefix="/varietas",
    tags=["Varietas"]
)


@router.get("/")
def get_varietas(current_user: User = Depends(get_current_user)):

    db = SessionLocal()

    try:

        result = db.execute(
            text("""
                SELECT id,nama
                FROM varietas
                ORDER BY id
            """)
        )

        return [
            dict(row._mapping)
            for row in result
        ]

    finally:
        db.close()