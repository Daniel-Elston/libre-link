
INSERT INTO measurements (
    timestamp,
    type,
    value_mg_per_dl,
    measurement_colour,
    glucose_units,
    value,
    is_high,
    is_low
)
VALUES (
    %(timestamp)s,
    %(type)s,
    %(value_mg_per_dl)s,
    %(measurement_colour)s,
    %(glucose_units)s,
    %(value)s,
    %(is_high)s,
    %(is_low)s
) RETURNING measurement_id;
