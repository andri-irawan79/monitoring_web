from fastapi import APIRouter
from sqlalchemy import text

from database.session import SessionLocal

router = APIRouter(
    prefix="/varietas",
    tags=["Varietas"]
)


@router.get("/")
def get_varietas():

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