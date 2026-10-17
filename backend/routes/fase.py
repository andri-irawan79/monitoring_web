from fastapi import APIRouter
from sqlalchemy import text

from database.session import SessionLocal

router = APIRouter(
    prefix="/fase",
    tags=["Fase"]
)


@router.get("/")
def get_fase():

    db = SessionLocal()

    try:

        result = db.execute(
            text("""
                SELECT id,nama
                FROM fase_pertumbuhan
                ORDER BY id
            """)
        )

        return [
            dict(row._mapping)
            for row in result
        ]

    finally:
        db.close()