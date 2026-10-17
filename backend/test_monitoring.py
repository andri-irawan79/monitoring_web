from database.session import SessionLocal
from models.monitoring import Monitoring

db = SessionLocal()

data = db.query(Monitoring).all()

for row in data:
    print(
        row.id,
        row.nitrogen,
        row.ph
    )

db.close()