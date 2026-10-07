CREATE TABLE IF NOT EXISTS audit.pipeline_runs (
    run_id        BIGSERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100) NOT NULL,
    started_at    TIMESTAMP    NOT NULL DEFAULT now(),
    finished_at   TIMESTAMP,
    status        VARCHAR(20)  NOT NULL DEFAULT 'RUNNING'
        CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED')),
    rows_read     BIGINT,
    rows_written  BIGINT,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS audit.data_quality_results (
    check_id     BIGSERIAL PRIMARY KEY,
    check_name   VARCHAR(100) NOT NULL,
    table_name   VARCHAR(150),
    status       VARCHAR(10)  NOT NULL CHECK (status IN ('PASS', 'FAIL')),
    failed_rows  BIGINT DEFAULT 0,
    details      TEXT,
    checked_at   TIMESTAMP NOT NULL DEFAULT now()
);