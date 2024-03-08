
INSERT INTO live_measurements (
    timestamp,
    type,
    value_mg_per_dl,
    measurement_colour,
    glucose_units,
    value,
    is_high,
    is_low,
    trend_arrow,
    trend_message
)
VALUES (
    %(timestamp)s,
    %(type)s,
    %(value_mg_per_dl)s,
    %(measurement_colour)s,
    %(glucose_units)s,
    %(value)s,
    %(is_high)s,
    %(is_low)s,
    %(trend_arrow)s,
    %(trend_message)s
);
