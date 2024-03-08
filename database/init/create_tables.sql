CREATE SCHEMA IF NOT EXISTS libre_link;

-- Switch to the schema
SET search_path TO libre_link;

CREATE TABLE IF NOT EXISTS live_measurements (
    measurement_id SERIAL PRIMARY KEY,
    factory_timestamp TIMESTAMP,
    timestamp TIMESTAMP,
    type INTEGER,
    value_mg_per_dl INTEGER,
    measurement_colour INTEGER,
    glucose_units INTEGER,
    value FLOAT,
    is_high BOOLEAN,
    is_low BOOLEAN,
    trend_arrow INTEGER,
    trend_message TEXT
);

-- Indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_timestamp ON live_measurements (timestamp);
