from __future__ import annotations

import logging

import psycopg2

from database.utils_db.db_ops import prepare_measurements
from utils.file_utils import load_sql
from utils.setup_env import setup_project_env
project_dir, _, _, db_config = setup_project_env()


def insert_to_db(data, my_pool):
    """Insert data into the database."""
    # pgsql_pool = create_my_pool(db_config)
    conn = my_pool.getconn()

    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SET search_path TO libre_link")

            # Prepare and insert measurements
            measurements_insert_path = project_dir / 'database/insert/measurements.sql'
            measurements_insert_sql = load_sql(measurements_insert_path)
            measurements_to_insert = prepare_measurements(data)

            for measurement in measurements_to_insert:
                cur.execute(measurements_insert_sql, measurement)
            conn.commit()
            logging.info("Data inserted successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            conn.rollback()
            logging.error(f"Failed to insert data: {error}")
        finally:
            cur.close()
            my_pool.putconn(conn)
