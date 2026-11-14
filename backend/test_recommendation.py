from services.recommendation_service import (
    generate_recommendation
)

hasil = generate_recommendation(
    monitoring_id=1,
    fase_id=1
)

print(hasil)
