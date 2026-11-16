-- Migrasi Alternatif B:
-- menghapus master varietas karena objek penelitian tetap Durian Montong.
--
-- WAJIB:
-- 1. Hentikan backend.
-- 2. Buat backup penuh PostgreSQL sebelum menjalankan skrip:
--    pg_dump -Fc -d NAMA_DATABASE -f before_remove_varietas.dump
-- 3. Pastikan skrip dijalankan pada database dan schema yang benar.
--
-- Skrip mengarsipkan mapping varietas lama per rekomendasi ke tabel
-- rekomendasi_varietas_archive sebelum melepas kolom dan master tabel.
-- Jika ada tabel lain yang masih mereferensikan varietas, skrip gagal
-- dan transaksi di-rollback. Skrip tidak memakai CASCADE.

BEGIN;

CREATE TABLE IF NOT EXISTS public.rekomendasi_varietas_archive (
    rekomendasi_id INTEGER PRIMARY KEY,
    varietas_id_lama INTEGER,
    nama_varietas_lama VARCHAR(150),
    archived_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

DO $migration$
DECLARE
    has_rekomendasi_varietas_id BOOLEAN;
    has_varietas_table BOOLEAN;
    fk_name TEXT;
    remaining_reference BOOLEAN;
BEGIN
    has_rekomendasi_varietas_id := EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'rekomendasi'
          AND column_name = 'varietas_id'
    );

    has_varietas_table := to_regclass('public.varietas') IS NOT NULL;

    IF has_rekomendasi_varietas_id THEN
        IF has_varietas_table THEN
            INSERT INTO public.rekomendasi_varietas_archive (
                rekomendasi_id,
                varietas_id_lama,
                nama_varietas_lama
            )
            SELECT
                r.id,
                r.varietas_id,
                v.nama
            FROM public.rekomendasi AS r
            LEFT JOIN public.varietas AS v
                ON v.id = r.varietas_id
            ON CONFLICT (rekomendasi_id) DO UPDATE
            SET
                varietas_id_lama = EXCLUDED.varietas_id_lama,
                nama_varietas_lama = EXCLUDED.nama_varietas_lama;
        ELSE
            INSERT INTO public.rekomendasi_varietas_archive (
                rekomendasi_id,
                varietas_id_lama,
                nama_varietas_lama
            )
            SELECT
                r.id,
                r.varietas_id,
                NULL
            FROM public.rekomendasi AS r
            ON CONFLICT (rekomendasi_id) DO NOTHING;
        END IF;

        IF has_varietas_table THEN
            FOR fk_name IN
                SELECT conname
                FROM pg_constraint
                WHERE contype = 'f'
                  AND conrelid = 'public.rekomendasi'::regclass
                  AND confrelid = 'public.varietas'::regclass
            LOOP
                EXECUTE format(
                    'ALTER TABLE public.rekomendasi DROP CONSTRAINT %I',
                    fk_name
                );
            END LOOP;
        END IF;

        ALTER TABLE public.rekomendasi
            DROP COLUMN IF EXISTS varietas_id;
    END IF;

    IF has_varietas_table THEN
        SELECT EXISTS (
            SELECT 1
            FROM pg_constraint
            WHERE contype = 'f'
              AND confrelid = 'public.varietas'::regclass
        )
        INTO remaining_reference;

        IF remaining_reference THEN
            RAISE EXCEPTION
                'Tabel public.varietas masih direferensikan tabel lain. '
                'Periksa foreign key yang tersisa dan migrasikan relasi tersebut terlebih dahulu.';
        END IF;

        DROP TABLE public.varietas;
    END IF;
END
$migration$;

COMMIT;

-- Verifikasi setelah migrasi:
-- 1. SELECT to_regclass('public.varietas'); -- harus NULL
-- 2. Pastikan rekomendasi.varietas_id tidak lagi ada:
--    SELECT column_name FROM information_schema.columns
--    WHERE table_schema='public' AND table_name='rekomendasi';
-- 3. Periksa arsip riwayat:
--    SELECT * FROM public.rekomendasi_varietas_archive
--    ORDER BY rekomendasi_id;
