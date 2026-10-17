from database.session import SessionLocal

from models.monitoring import Monitoring
from models.rekomendasi import Rekomendasi

from fuzzy.tsukamoto import (
    fuzzifikasi,
    evaluate_phase,
    defuzzifikasi
)

from fuzzy.variety_factor import (
    koreksi_varietas
)


FASE_MAP = {

    1: "Vegetatif",
    2: "Pembungaan",
    3: "Pembuahan",
    4: "Panen",
    5: "Pascapanen"
}


def generate_recommendation(
    monitoring_id,
    varietas_id,
    fase_id
):

    db = SessionLocal()

    try:

        # Ambil data monitoring
        monitoring = (
            db.query(Monitoring)
            .filter(
                Monitoring.id == monitoring_id
            )
            .first()
        )

        if not monitoring:

            return {
                "success": False,
                "message": "Data monitoring tidak ditemukan"
            }

        # Fuzzifikasi
        fuzzy_values = fuzzifikasi(

            monitoring.nitrogen,
            monitoring.phosphorus,
            monitoring.potassium,
            monitoring.ph
        )

        # Nama fase
        fase_nama = FASE_MAP.get(fase_id)

        if not fase_nama:

            return {
                "success": False,
                "message": "Fase tidak valid"
            }

        # Evaluasi rule
        results = evaluate_phase(

            fase_nama,
            fuzzy_values
        )

        if len(results) == 0:

            return {
                "success": False,
                "message": "Tidak ada rule yang aktif"
            }

        # Defuzzifikasi
        defuzz = defuzzifikasi(results)
        dosis = defuzz["hasil"]
        
        # Rule dominan
        best_rule = max(

            results,

            key=lambda x: x["alpha"]
        )

        # Koreksi varietas
        dosis_final = koreksi_varietas(

            dosis,

            varietas_id
        )

        # Simpan rekomendasi
        rekomendasi = Rekomendasi(

            monitoring_id=monitoring_id,

            varietas_id=varietas_id,

            fase_id=fase_id,

            jenis_pupuk=best_rule["pupuk"],

            dosis=round(
                dosis_final,
                2
            ),

            kategori=best_rule["output"]
        )

        db.add(rekomendasi)

        db.commit()

        db.refresh(rekomendasi)

        return {

                "success": True,

                "recommendation": {

                    "id": rekomendasi.id,

                    "jenis_pupuk": rekomendasi.jenis_pupuk,

                    "dosis": rekomendasi.dosis,

                    "kategori": rekomendasi.kategori

                },

                "fuzzy_values": fuzzy_values,

                "best_rule": best_rule,

                "active_rules": results,

                "defuzzification": defuzz

            }

    except Exception as e:

        db.rollback()

        return {

            "success": False,

            "message": str(e)
        }

    finally:

        db.close()