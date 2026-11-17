from fastapi import FastAPI
from sqlalchemy import inspect, text
from database.connection import engine
from models.user import User
from models.simulation_session import SimulationSession
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
            "Tabel 'monitoring' belum tersedia. Siapkan skema monitoring "
            "yang digunakan aplikasi sebelum menjalankan server."
        )
    if not inspector.has_table("rekomendasi"):
        raise RuntimeError(
            "Tabel 'rekomendasi' belum tersedia. Siapkan skema rekomendasi "
            "yang digunakan aplikasi sebelum menjalankan server."
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
            "ADD COLUMN IF NOT EXISTS user_id INTEGER "
            "REFERENCES users(id) ON DELETE CASCADE"
        ))
        connection.execute(text(
            "ALTER TABLE rekomendasi "
            "ADD COLUMN IF NOT EXISTS user_id INTEGER "
            "REFERENCES users(id) ON DELETE CASCADE"
        ))

        # Recommendation records must survive deletion of their monitoring
        # snapshot. Store the recommendation result, but detach its optional
        # monitoring reference so historical fertilizer output is preserved.
        connection.execute(text(
            "ALTER TABLE rekomendasi "
            "ALTER COLUMN monitoring_id DROP NOT NULL"
        ))
        connection.execute(text("""
            DO $migration$
            DECLARE
                fk_name TEXT;
            BEGIN
                FOR fk_name IN
                    SELECT conname
                    FROM pg_constraint
                    WHERE contype = 'f'
                      AND conrelid = 'public.rekomendasi'::regclass
                      AND confrelid = 'public.monitoring'::regclass
                LOOP
                    EXECUTE format(
                        'ALTER TABLE public.rekomendasi DROP CONSTRAINT %I',
                        fk_name
                    );
                END LOOP;

                IF NOT EXISTS (
                    SELECT 1
                    FROM pg_constraint
                    WHERE conname = 'fk_rekomendasi_monitoring_set_null'
                      AND conrelid = 'public.rekomendasi'::regclass
                ) THEN
                    ALTER TABLE public.rekomendasi
                        ADD CONSTRAINT fk_rekomendasi_monitoring_set_null
                        FOREIGN KEY (monitoring_id)
                        REFERENCES public.monitoring(id)
                        ON DELETE SET NULL;
                END IF;
            END
            $migration$;
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
