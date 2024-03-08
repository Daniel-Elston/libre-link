from __future__ import annotations

from database.utils_db.connection import create_my_engine
from database.utils_db.db_ops import prepare_measurements
from utils.file_utils import load_sql
from utils.setup_env import setup_project_env
project_dir, config, setup_logs = setup_project_env()


def insert_to_db(data):
    _, conn = create_my_engine(config)
    cur = conn.cursor()
    cur.execute("SET search_path TO libre_link")

    # Prepare and insert measurements
    measurements_insert_path = project_dir / 'database/insert/measurements.sql'
    measurements_insert_sql = load_sql(measurements_insert_path)
    measurements_to_insert = prepare_measurements(data)

    for measurement in measurements_to_insert:
        cur.execute(measurements_insert_sql, measurement)
        conn.commit()

    cur.close()
    conn.close()
