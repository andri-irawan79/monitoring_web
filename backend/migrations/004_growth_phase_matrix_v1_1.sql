-- Revisi fase dan matriks prioritas NPK v1.1.
-- Backup database sebelum menjalankan migrasi.
-- ID fase dipertahankan agar foreign key rekomendasi lama tetap valid.
-- Isi snapshot sebelum mengubah nama master agar riwayat lama tidak berubah.

BEGIN;

ALTER TABLE public.rekomendasi
    ADD COLUMN IF NOT EXISTS fase_nama_snapshot VARCHAR(50);

UPDATE public.rekomendasi r
SET fase_nama_snapshot = f.nama
FROM public.fase_pertumbuhan f
WHERE r.fase_id = f.id
  AND r.fase_nama_snapshot IS NULL;

UPDATE public.fase_pertumbuhan
SET nama = 'Prapembungaan'
WHERE id = 2 AND nama IN ('Pembungaan', 'Prapembungaan');

UPDATE public.fase_pertumbuhan
SET nama = 'Prapanen'
WHERE id = 4 AND nama IN ('Panen', 'Prapanen');

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM public.fase_pertumbuhan
        WHERE id = 2 AND nama = 'Prapembungaan'
    ) THEN
        RAISE EXCEPTION 'Fase id=2 tidak ditemukan atau namanya tidak sesuai; periksa master fase.';
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM public.fase_pertumbuhan
        WHERE id = 4 AND nama = 'Prapanen'
    ) THEN
        RAISE EXCEPTION 'Fase id=4 tidak ditemukan atau namanya tidak sesuai; periksa master fase.';
    END IF;
END $$;

COMMIT;

-- Verifikasi:
-- SELECT id, nama FROM public.fase_pertumbuhan ORDER BY id;
-- SELECT fase_nama_snapshot, COUNT(*) FROM public.rekomendasi
-- GROUP BY fase_nama_snapshot ORDER BY fase_nama_snapshot;
