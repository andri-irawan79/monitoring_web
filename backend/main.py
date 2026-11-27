from fastapi import FastAPI
from sqlalchemy import inspect, text
from database.connection import engine
from models.user import User
from models.simulation_session import SimulationSession
from models.rekomendasi_detail import RekomendasiDetail
from routes.auth import router as auth_router
from routes.monitoring import router as monitoring_router
from routes.fase import router as fase_router
from routes.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware
from routes.recommendation import (
    router as recommendation_router
)

app = FastAPI(title="Durian Monitoring API")


@app.on_event("startup")
def prepare_application_tables():
    # Membuat tabel akun baru. Jika ada tabel users versi lama,
    # hentikan startup dengan pesan yang jelas; create(checkfirst=True)
    # tidak mengubah struktur tabel yang sudah ada.
    inspector = inspect(engine)
    if inspector.has_table("users"):
        existing_columns = {
            column["name"] for column in inspector.get_columns("users")
        }
        required_columns = {
            "id", "full_name", "email", "password_hash", "is_active", "created_at"
        }
        missing_columns = required_columns - existing_columns
        if missing_columns:
            missing_text = ", ".join(sorted(missing_columns))
            raise RuntimeError(
                "Tabel 'users' yang sudah ada memakai skema lama. "
                f"Kolom yang dibutuhkan autentikasi belum tersedia: {missing_text}. "
                "Cadangkan data terlebih dahulu, lalu lakukan migrasi atau ubah nama "
                "tabel lama sebelum menjalankan aplikasi."
            )
    else:
        User.__table__.create(bind=engine, checkfirst=True)

    inspector = inspect(engine)
    if not inspector.has_table("monitoring"):
        raise RuntimeError(
            "Tabel 'monitoring' belum tersedia. Jalankan migrations/000_base_schema.sql "
            "(atau docker compose up) sebelum menjalankan server."
        )
    if not inspector.has_table("rekomendasi"):
        raise RuntimeError(
            "Tabel 'rekomendasi' belum tersedia. Jalankan migrations/000_base_schema.sql "
            "(atau docker compose up) sebelum menjalankan server."
        )

    # Create the new session table if needed; all owner columns are nullable
    # for legacy records whose original account cannot be determined safely.
    SimulationSession.__table__.create(bind=engine, checkfirst=True)

    with engine.begin() as connection:
        # Older user tables receive a default authentication version without
        # requiring manual data updates. Existing tokens use version zero.
        connection.execute(text(
            "ALTER TABLE users "
            "ADD COLUMN IF NOT EXISTS auth_version INTEGER NOT NULL DEFAULT 0"
        ))

        connection.execute(text(
            "ALTER TABLE monitoring "
            "ADD COLUMN IF NOT EXISTS simulation_session_id VARCHAR(36)"
        ))
        connection.execute(text(
            "ALTER TABLE monitoring "
            "ADD COLUMN IF NOT EXISTS session_record_number INTEGER"
        ))
        connection.execute(text(
            "ALTER TABLE monitoring "
            "ADD COLUMN IF NOT EXISTS soil_moisture DOUBLE PRECISION"
        ))

        connection.execute(text(
            "ALTER TABLE monitoring "
            "ADD COLUMN IF NOT EXISTS user_id INTEGER "
            "REFERENCES users(id) ON DELETE CASCADE"
        ))
        connection.execute(text(
            "ALTER TABLE rekomendasi "
            "ADD COLUMN IF NOT EXISTS user_id INTEGER "
            "REFERENCES users(id) ON DELETE CASCADE"
        ))
        connection.execute(text(
            "ALTER TABLE rekomendasi "
            "ADD COLUMN IF NOT EXISTS fase_nama_snapshot VARCHAR(50)"
        ))
        connection.execute(text("""
            UPDATE rekomendasi r
            SET fase_nama_snapshot = f.nama
            FROM fase_pertumbuhan f
            WHERE r.fase_id = f.id
              AND r.fase_nama_snapshot IS NULL
        """))

        # FIS-1/FIS-2: keep legacy recommendation fields readable while allowing
        # one recommendation header to contain multiple fertilizer details.
        connection.execute(text("""
            ALTER TABLE rekomendasi
            ADD COLUMN IF NOT EXISTS algorithm_version VARCHAR(40) NOT NULL DEFAULT 'legacy',
            ADD COLUMN IF NOT EXISTS fuzzy_trace JSONB NOT NULL DEFAULT '{}'::jsonb,
            ADD COLUMN IF NOT EXISTS z_n DOUBLE PRECISION,
            ADD COLUMN IF NOT EXISTS z_p DOUBLE PRECISION,
            ADD COLUMN IF NOT EXISTS z_k DOUBLE PRECISION,
            ADD COLUMN IF NOT EXISTS z_dolomit DOUBLE PRECISION,
            ADD COLUMN IF NOT EXISTS z_belerang DOUBLE PRECISION
        """))
        connection.execute(text(
            "ALTER TABLE rekomendasi "
            "ALTER COLUMN jenis_pupuk DROP NOT NULL, "
            "ALTER COLUMN dosis DROP NOT NULL, "
            "ALTER COLUMN kategori DROP NOT NULL"
        ))

        # Route riwayat, terbaru, dan hapus melakukan JOIN ke tabel arsip ini. Sebelumnya tabel
        # hanya dibuat oleh migrasi 001, sehingga instalasi baru error. Idempoten dan sama dengan 001/000.
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS public.rekomendasi_varietas_archive (
                rekomendasi_id INTEGER PRIMARY KEY,
                varietas_id_lama INTEGER,
                nama_varietas_lama VARCHAR(150),
                archived_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
            )
        """))

        connection.execute(text(
            "ALTER TABLE simulation_sessions "
            "ADD COLUMN IF NOT EXISTS user_id INTEGER "
            "REFERENCES users(id) ON DELETE CASCADE"
        ))

        connection.execute(text(
            "UPDATE rekomendasi r "
            "SET user_id = m.user_id "
            "FROM monitoring m "
            "WHERE r.monitoring_id = m.id "
            "AND r.user_id IS NULL "
            "AND m.user_id IS NOT NULL"
        ))

        connection.execute(text(
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_monitoring_session_record "
            "ON monitoring (simulation_session_id, session_record_number) "
            "WHERE simulation_session_id IS NOT NULL "
            "AND session_record_number IS NOT NULL"
        ))
        connection.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_monitoring_user_id "
            "ON monitoring (user_id)"
        ))
        connection.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_rekomendasi_user_id "
            "ON rekomendasi (user_id)"
        ))
        connection.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_simulation_sessions_user_id "
            "ON simulation_sessions (user_id)"
        ))

        # The old index allowed only one active session for the whole app.
        # Replace it with a per-user constraint.
        connection.execute(text(
            "DROP INDEX IF EXISTS uq_simulation_sessions_single_active"
        ))
        connection.execute(text(
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_simulation_sessions_single_active_user "
            "ON simulation_sessions (user_id) "
            "WHERE user_id IS NOT NULL "
            "AND status IN ('starting', 'running')"
        ))

    # The migration is additive and safe to re-run. It is also represented by
    # backend/migrations/002_fis1_fis2_multi_fertilizer.sql for explicit DB rollout.
    RekomendasiDetail.__table__.create(bind=engine, checkfirst=True)


app.include_router(auth_router)

app.include_router(
    monitoring_router,
    prefix="/monitoring",
    tags=["Monitoring"]
)

app.include_router(
    recommendation_router,
    prefix="/recommendation"
)

app.include_router(fase_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "message": "Durian Monitoring API"
    }


# Wrap the complete ASGI application so CORS headers are also attached to
# error responses raised outside the route exception handlers (for example,
# database errors). Keep this as the final app assignment so route decorators
# above are registered on the FastAPI instance before it is wrapped.
app = CORSMiddleware(
    app=app,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
