from sqlalchemy import text

from database.session import SessionLocal

from models.monitoring import Monitoring
from models.rekomendasi import Rekomendasi

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

VARIETAS_TETAP = "Montong"


def generate_recommendation(
    monitoring_id,
    fase_id
):
    """
    Menghasilkan rekomendasi khusus durian Montong.

    Varietas tidak menjadi variabel fuzzy dan tidak digunakan sebagai
    faktor pengali dosis. ID Montong hanya disimpan sebagai metadata
    objek penelitian pada tabel rekomendasi.
    """

    db = SessionLocal()

    try:
        monitoring = (
            db.query(Monitoring)
            .filter(Monitoring.id == monitoring_id)
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
                "message": "Fase tidak valid"
            }

        # Cari ID objek varietas Montong untuk metadata riwayat.
        # Nilai ini tidak digunakan dalam proses perhitungan dosis.
        montong_row = db.execute(
            text("""
                SELECT id
                FROM varietas
                WHERE LOWER(TRIM(nama)) = LOWER(:nama)
                ORDER BY id
                LIMIT 1
            """),
            {"nama": VARIETAS_TETAP}
        ).first()

        if montong_row is None:
            return {
                "success": False,
                "message": (
                    "Data master varietas Durian Montong "
                    "tidak ditemukan"
                )
            }

        montong_id = montong_row[0]

        fuzzy_values = fuzzifikasi(
            monitoring.nitrogen,
            monitoring.phosphorus,
            monitoring.potassium,
            monitoring.ph
        )

        results = evaluate_phase(
            fase_nama,
            fuzzy_values
        )

        if not results:
            return {
                "success": False,
                "message": "Tidak ada rule yang aktif"
            }

        defuzz = defuzzifikasi(results)
        dosis_final = defuzz["hasil"]

        best_rule = max(
            results,
            key=lambda item: item["alpha"]
        )

        # Dosis digunakan langsung dari hasil defuzzifikasi.
        # Tidak ada koreksi atau perkalian berdasarkan varietas.
        rekomendasi = Rekomendasi(
            monitoring_id=monitoring_id,
            varietas_id=montong_id,
            fase_id=fase_id,
            jenis_pupuk=best_rule["pupuk"],
            dosis=round(dosis_final, 2),
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
                "kategori": rekomendasi.kategori,
                "varietas": VARIETAS_TETAP
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
