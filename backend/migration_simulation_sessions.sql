-- Durian Monitor: per-session simulator progress.
-- Run against the application's PostgreSQL database before deploying
-- if automatic startup schema preparation is disabled in your environment.
CREATE TABLE IF NOT EXISTS simulation_sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id INTEGER NULL REFERENCES users(id) ON DELETE CASCADE,
    mode VARCHAR(16) NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'starting',
    target_count INTEGER NOT NULL DEFAULT 365,
    received_count INTEGER NOT NULL DEFAULT 0,
    started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    last_received_at TIMESTAMP WITHOUT TIME ZONE NULL,
    finished_at TIMESTAMP WITHOUT TIME ZONE NULL,
    process_id INTEGER NULL,
    error_message TEXT NULL
);

ALTER TABLE monitoring
    ADD COLUMN IF NOT EXISTS simulation_session_id VARCHAR(36) NULL;

ALTER TABLE monitoring
    ADD COLUMN IF NOT EXISTS session_record_number INTEGER NULL;

ALTER TABLE simulation_sessions
    ADD COLUMN IF NOT EXISTS user_id INTEGER NULL
    REFERENCES users(id) ON DELETE CASCADE;

DROP INDEX IF EXISTS uq_simulation_sessions_single_active;

CREATE UNIQUE INDEX IF NOT EXISTS uq_monitoring_session_record
    ON monitoring (simulation_session_id, session_record_number)
    WHERE simulation_session_id IS NOT NULL
      AND session_record_number IS NOT NULL;

-- A session is active independently for each authenticated account.
CREATE UNIQUE INDEX IF NOT EXISTS uq_simulation_sessions_single_active_user
    ON simulation_sessions (user_id)
    WHERE user_id IS NOT NULL
      AND status IN ('starting', 'running');
