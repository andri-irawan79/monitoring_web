from database.session import SessionLocal
from models.monitoring import Monitoring
from models.rekomendasi import Rekomendasi
from constants import PLANT_VARIETY, PLANT_DISPLAY_NAME

from fuzzy.tsukamoto import (
    fuzzifikasi,
    evaluate_phase,
    defuzzifikasi
)


FASE_MAP = {
    1: "Vegetatif",
    2: "Pembungaan",
    3: "Pembuahan",
    4: "Panen",
    5: "Pascapanen"
}


def generate_recommendation(monitoring_id, fase_id, user_id):
    """
    Menghasilkan rekomendasi untuk objek tetap penelitian, yaitu
    tanaman durian varietas Montong. Identitas varietas merupakan
    konfigurasi aplikasi, bukan master data maupun variabel fuzzy.
    """
    db = SessionLocal()
    try:
        monitoring = (
            db.query(Monitoring)
            .filter(
                Monitoring.id == monitoring_id,
                Monitoring.user_id == user_id,
            )
            .first()
        )
        if not monitoring:
            return {
                "success": False,
                "message": "Data monitoring tidak ditemukan"
            }

        fase_nama = FASE_MAP.get(fase_id)
        if not fase_nama:
            return {
                "success": False,
                "message": "Fase pertumbuhan tidak valid"
            }

        fuzzy_values = fuzzifikasi(
            monitoring.nitrogen,
            monitoring.phosphorus,
            monitoring.potassium,
            monitoring.ph
        )
        results = evaluate_phase(fase_nama, fuzzy_values)
        if not results:
            return {
                "success": False,
                "message": "Tidak ada rule yang aktif untuk kondisi input tersebut"
            }

        defuzz = defuzzifikasi(results)
        best_rule = max(results, key=lambda item: item["alpha"])

        # Dosis berasal langsung dari hasil defuzzifikasi.
        # Tidak ada pencarian ID varietas atau koreksi varietas.
        recommendation = Rekomendasi(
            user_id=user_id,
            monitoring_id=monitoring_id,
            fase_id=fase_id,
            jenis_pupuk=best_rule["pupuk"],
            dosis=round(defuzz["hasil"], 2),
            kategori=best_rule["output"]
        )
        db.add(recommendation)
        db.commit()
        db.refresh(recommendation)

        return {
            "success": True,
            "recommendation": {
                "id": recommendation.id,
                "jenis_pupuk": recommendation.jenis_pupuk,
                "dosis": recommendation.dosis,
                "kategori": recommendation.kategori,
                "varietas": PLANT_VARIETY,
                "objek_tanaman": PLANT_DISPLAY_NAME,
                "fase": fase_nama,
                "created_at": recommendation.created_at
            },
            "fuzzy_values": fuzzy_values,
            "best_rule": best_rule,
            "active_rules": results,
            "defuzzification": defuzz
        }
    except Exception as error:
        db.rollback()
        return {
            "success": False,
            "message": str(error)
        }
    finally:
        db.close()
