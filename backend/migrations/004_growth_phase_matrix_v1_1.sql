-- Revisi nama fase dan matriks prioritas NPK v1.1.
-- Jalankan setelah backup database.
-- Migrasi mempertahankan fase_id sehingga foreign key rekomendasi lama tetap valid.
-- Snapshot yang sudah terisi tidak ditimpa agar label historis tetap terjaga.
-- Pemetaan ID tidak diasumsikan: perubahan dilakukan berdasarkan nama fase lama.

BEGIN;

ALTER TABLE public.rekomendasi
    ADD COLUMN IF NOT EXISTS fase_nama_snapshot VARCHAR(50);

-- Simpan nama fase historis hanya untuk rekomendasi yang belum memiliki snapshot.
UPDATE public.rekomendasi r
SET fase_nama_snapshot = f.nama
FROM public.fase_pertumbuhan f
WHERE r.fase_id = f.id
  AND r.fase_nama_snapshot IS NULL;

-- Hindari konflik UNIQUE apabila nama lama dan nama tujuan sama-sama sudah ada.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM public.fase_pertumbuhan fase_lama
        JOIN public.fase_pertumbuhan fase_tujuan
          ON LOWER(BTRIM(fase_tujuan.nama)) =
             CASE LOWER(BTRIM(fase_lama.nama))
                 WHEN 'panen' THEN 'prapanen'
                 WHEN 'pembungaan' THEN 'prapembungaan'
             END
        WHERE LOWER(BTRIM(fase_lama.nama)) IN ('panen', 'pembungaan')
    ) THEN
        RAISE EXCEPTION
            'Migrasi fase dibatalkan: nama fase lama dan nama tujuan ditemukan bersamaan. Periksa tabel fase_pertumbuhan terlebih dahulu.';
    END IF;
END $$;

-- Normalisasi berdasarkan nama, bukan ID yang dapat berbeda antar database.
UPDATE public.fase_pertumbuhan
SET nama = CASE LOWER(BTRIM(nama))
    WHEN 'panen' THEN 'Prapanen'
    WHEN 'pembungaan' THEN 'Prapembungaan'
    ELSE nama
END
WHERE LOWER(BTRIM(nama)) IN ('panen', 'pembungaan');

-- Pastikan master fase berisi tepat lima fase yang digunakan aplikasi.
DO $$
DECLARE
    jumlah_fase INTEGER;
BEGIN
    SELECT COUNT(*) INTO jumlah_fase
    FROM public.fase_pertumbuhan;

    IF jumlah_fase <> 5 THEN
        RAISE EXCEPTION
            'Validasi fase gagal: diharapkan 5 fase, ditemukan %.', jumlah_fase;
    END IF;

    IF EXISTS (
        SELECT fase_wajib.nama
        FROM (VALUES
            ('vegetatif'),
            ('prapembungaan'),
            ('pembuahan'),
            ('prapanen'),
            ('pascapanen')
        ) AS fase_wajib(nama)
        LEFT JOIN public.fase_pertumbuhan f
          ON LOWER(BTRIM(f.nama)) = fase_wajib.nama
        GROUP BY fase_wajib.nama
        HAVING COUNT(f.id) <> 1
    ) THEN
        RAISE EXCEPTION
            'Validasi fase gagal: master harus berisi Vegetatif, Prapembungaan, Pembuahan, Prapanen, dan Pascapanen masing-masing satu kali.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM public.fase_pertumbuhan
        WHERE LOWER(BTRIM(nama)) IN ('panen', 'pembungaan')
    ) THEN
        RAISE EXCEPTION
            'Validasi fase gagal: nama fase lama Panen/Pembungaan masih ditemukan.';
    END IF;
END $$;

COMMIT;

-- Verifikasi setelah migrasi:
-- SELECT id, nama FROM public.fase_pertumbuhan ORDER BY id;
-- SELECT fase_nama_snapshot, COUNT(*) FROM public.rekomendasi
-- GROUP BY fase_nama_snapshot ORDER BY fase_nama_snapshot;
