-- Isolate monitoring, recommendation, and simulation data by account.
-- Existing records are retained with user_id = NULL because their original
-- owner cannot be inferred safely. They are excluded from every user's views.
-- Back up the database before applying this migration manually.

ALTER TABLE monitoring
    ADD COLUMN IF NOT EXISTS user_id INTEGER
    REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE rekomendasi
    ADD COLUMN IF NOT EXISTS user_id INTEGER
    REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE simulation_sessions
    ADD COLUMN IF NOT EXISTS user_id INTEGER
    REFERENCES users(id) ON DELETE CASCADE;

-- When historical monitoring records are explicitly assigned to an account
-- later, their recommendation records can inherit the same owner.
UPDATE rekomendasi r
SET user_id = m.user_id
FROM monitoring m
WHERE r.monitoring_id = m.id
  AND r.user_id IS NULL
  AND m.user_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_monitoring_user_id
    ON monitoring (user_id);

CREATE INDEX IF NOT EXISTS ix_rekomendasi_user_id
    ON rekomendasi (user_id);

CREATE INDEX IF NOT EXISTS ix_simulation_sessions_user_id
    ON simulation_sessions (user_id);

-- Replace the previous global single-active-session constraint with one
-- active session per account. This allows two users to simulate independently.
DROP INDEX IF EXISTS uq_simulation_sessions_single_active;

CREATE UNIQUE INDEX IF NOT EXISTS uq_simulation_sessions_single_active_user
    ON simulation_sessions (user_id)
    WHERE user_id IS NOT NULL
      AND status IN ('starting', 'running');
