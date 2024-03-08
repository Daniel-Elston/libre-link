INSERT INTO trends (
    measurement_id,
    timestamp,
    trend_arrow,
    trend_message
)
VALUES (
    %(measurement_id)s,
    %(timestamp)s,
    %(trend_arrow)s,
    %(trend_message)s
);
