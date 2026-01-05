-- Schema placeholder for SQLite migrations
CREATE TABLE IF NOT EXISTS feature_vectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schema_id TEXT NOT NULL,
    values_json TEXT NOT NULL
);
