-- 000_base_schema.sql : skema dasar untuk INSTALASI BARU (basis data kosong). Idempoten: aman dijalankan ulang.
-- Urutan instalasi baru:  000 -> 002 -> 003   (001 hanya untuk basis data lama yang masih memiliki master varietas).
-- Tabel simulation_sessions dibuat oleh aplikasi saat startup (models/simulation_session.py).
BEGIN;

CREATE TABLE IF NOT EXISTS public.users (
    id            SERIAL PRIMARY KEY,
    full_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    auth_version  INTEGER      NOT NULL DEFAULT 0,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON public.users (email);

-- Urutan id mengikuti pemetaan historis (rekomendasi lama menyimpan fase_id).
CREATE TABLE IF NOT EXISTS public.fase_pertumbuhan (
    id   INTEGER PRIMARY KEY,
    nama VARCHAR(50) NOT NULL UNIQUE
);
INSERT INTO public.fase_pertumbuhan (id, nama) VALUES
    (1, 'Vegetatif'), (2, 'Prapembungaan'), (3, 'Pembuahan'), (4, 'Prapanen'), (5, 'Pascapanen')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS public.monitoring (
    id                    SERIAL PRIMARY KEY,
    nitrogen              DOUBLE PRECISION,
    phosphorus            DOUBLE PRECISION,
    potassium             DOUBLE PRECISION,
    temperature           DOUBLE PRECISION,
    humidity              DOUBLE PRECISION,
    ph                    DOUBLE PRECISION CHECK (ph IS NULL OR ph BETWEEN 0 AND 14),
    soil_moisture         DOUBLE PRECISION CHECK (soil_moisture IS NULL OR soil_moisture BETWEEN 0 AND 100),
    rainfall              DOUBLE PRECISION,
    created_at            TIMESTAMP DEFAULT now(),
    simulation_date       DATE,
    user_id               INTEGER REFERENCES public.users(id) ON DELETE CASCADE,
    simulation_session_id VARCHAR(36),
    session_record_number INTEGER
);

CREATE TABLE IF NOT EXISTS public.rekomendasi (
    id            SERIAL PRIMARY KEY,
    user_id       INTEGER REFERENCES public.users(id) ON DELETE CASCADE,
    monitoring_id INTEGER NOT NULL,
    fase_id       INTEGER NOT NULL REFERENCES public.fase_pertumbuhan(id),
    fase_nama_snapshot VARCHAR(50),
    jenis_pupuk   VARCHAR,
    dosis         DOUBLE PRECISION,
    kategori      VARCHAR,
    created_at    TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.rekomendasi_varietas_archive (
    rekomendasi_id     INTEGER PRIMARY KEY,
    varietas_id_lama   INTEGER,
    nama_varietas_lama VARCHAR(150),
    archived_at        TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

COMMIT;
