CREATE SCHEMA IF NOT EXISTS libre_link;

-- Switch to the schema
SET search_path TO libre_link;

CREATE TABLE IF NOT EXISTS measurements (
    measurement_id SERIAL PRIMARY KEY,
    factory_timestamp TIMESTAMP,
    timestamp TIMESTAMP,
    type INTEGER,
    value_mg_per_dl INTEGER,
    measurement_colour INTEGER,
    glucose_units INTEGER,
    value FLOAT,
    is_high BOOLEAN,
    is_low BOOLEAN
);

CREATE TABLE IF NOT EXISTS trends (
    trend_id SERIAL PRIMARY KEY,
    measurement_id INTEGER NOT NULL,
    timestamp TIMESTAMP,
    trend_arrow INT,
    trend_message TEXT,
    CONSTRAINT fk_measurement
        FOREIGN KEY(measurement_id)
        REFERENCES measurements(measurement_id)
        ON DELETE CASCADE
);

-- Indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_timestamp ON measurements (timestamp);
CREATE INDEX IF NOT EXISTS idx_measurementid ON trends (measurement_id);
