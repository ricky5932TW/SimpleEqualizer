CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    finished_at TEXT NULL,
    run_type TEXT NOT NULL,
    params_json TEXT NULL,
    status TEXT NOT NULL,
    image_paths TEXT NULL,
    note TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_measurements_started_at
ON measurements(started_at);
