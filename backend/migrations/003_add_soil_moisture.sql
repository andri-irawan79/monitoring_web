-- Tambahkan kelembapan tanah sebagai parameter monitoring opsional.
-- Record historis tetap valid (NULL); simulator baru mengirim soil_moisture.
BEGIN;

ALTER TABLE public.monitoring
    ADD COLUMN IF NOT EXISTS soil_moisture DOUBLE PRECISION;

COMMIT;

-- Verifikasi:
-- SELECT column_name, data_type
-- FROM information_schema.columns
-- WHERE table_schema='public'
--   AND table_name='monitoring'
--   AND column_name='soil_moisture';
