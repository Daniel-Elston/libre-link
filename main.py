from __future__ import annotations

import atexit
import logging
import os
import time

import schedule

from database.pipeline import insert_to_db
from database.utils_db.connection import create_my_pool
from services.fetch_data import authenticate_and_fetch_data
from services.processing import process_timestamps
from utils.file_utils import append_json
from utils.setup_env import setup_project_env

# Environment setup
project_dir, config, setup_logs, db_config = setup_project_env()
pgsql_pool = create_my_pool(db_config)


def close_pool():
    """Close the connection pool on exit."""
    pgsql_pool.closeall()
    logging.info("Connection pool closed.")


atexit.register(close_pool)


def main():
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    # Authenticate and fetch data
    cgm_data = authenticate_and_fetch_data(email, password)
    glucose_measurement = cgm_data['data']['connection']['glucoseMeasurement']

    # Save data to local JSON store
    append_json(glucose_measurement, 'data/rt_data.json')

    # Process and insert data into the database
    process_timestamps([glucose_measurement])
    insert_to_db([glucose_measurement], pgsql_pool)


if __name__ == "__main__":
    logging.info("Starting the application...")
    schedule.every(1).minutes.do(main)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down...")
