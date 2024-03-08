from __future__ import annotations

import atexit
import logging
import time

import schedule

from database.database_management import DatabaseManagement
from services.auth_management import AuthenticationManagement
from services.data_management import DataManagement
from storage.storage_management import StorageManagement
from utils.setup_env import setup_project_env

# Environment setup
project_dir, config, setup_logs, db_config = setup_project_env()
atexit.register(DatabaseManagement(db_config).close_pool)


def main():
    """Main application function"""

    # Authentication
    auth_manager = AuthenticationManagement(config)
    token = auth_manager.login()
    patient_id = auth_manager.get_patient_id()

    # Fetch and access data
    data_manager = DataManagement(config, token, patient_id)
    glucose_measurement = data_manager.get_measurements()

    # Save data to local JSON store
    store_manager = StorageManagement()
    store_manager.append_json(glucose_measurement, 'rt_data.json')

    # Process data
    data_manager.process_timestamps(glucose_measurement)

    # Insert data into the database
    db_manager = DatabaseManagement(db_config)
    db_manager.insert_to_db(glucose_measurement)


if __name__ == "__main__":
    logging.info("Starting the application...")
    schedule.every(1).minutes.do(main)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down...")
