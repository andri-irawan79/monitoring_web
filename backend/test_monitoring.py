"""Manual monitoring inspection for one account.

Set TEST_USER_ID before running:
    TEST_USER_ID=1 python test_monitoring.py
"""
import os


def main():
    from database.session import SessionLocal
    from models.monitoring import Monitoring

    user_id = os.getenv("TEST_USER_ID")
    if not user_id:
        raise RuntimeError("Set TEST_USER_ID to the account ID to inspect.")

    db = SessionLocal()
    try:
        data = (
            db.query(Monitoring)
            .filter(Monitoring.user_id == int(user_id))
            .order_by(Monitoring.id.desc())
            .all()
        )
        for row in data:
            print(row.id, row.user_id, row.nitrogen, row.ph)
    finally:
        db.close()


if __name__ == "__main__":
    main()
