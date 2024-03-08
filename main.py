from __future__ import annotations

import os

from database.pipeline import insert_to_db
from services.fetch_data import authenticate_and_fetch_data
from services.processing import process_timestamps
from utils.file_utils import append_json
from utils.setup_env import setup_project_env
# import time
# import schedule

project_dir, config, setup_logs = setup_project_env()


def main():
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    cgm_data = authenticate_and_fetch_data(email, password)
    glucose_measurement = cgm_data['data']['connection']['glucoseMeasurement']

    append_json(glucose_measurement, 'data/rt_data.json')

    process_timestamps([glucose_measurement])

    insert_to_db([glucose_measurement])


if __name__ == "__main__":
    # schedule.every(1).minutes.do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    main()
