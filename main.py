from __future__ import annotations

import os
from datetime import datetime

from database.utils_db.connection import create_my_engine
from database.utils_db.db_ops import prepare_measurements
from database.utils_db.db_ops import prepare_trends
from services.fetch_data import get_cgm_data
from services.fetch_data import get_patient_connections
from services.fetch_data import login
from utils.file_utils import append_json
from utils.file_utils import load_from_json
from utils.file_utils import load_sql
from utils.setup_env import setup_project_env
# import time
# import schedule

project_dir, config, setup_logs = setup_project_env()


def get_dtype(data):
    if data:
        item_n = data[0]
        for key, value in item_n.items():
            print(f"{key}: {type(value)}")
    else:
        print("List is empty.")


def database_pipe(data):
    _, conn = create_my_engine(config)
    cur = conn.cursor()
    cur.execute("SET search_path TO libre_link")

    # Prepare and insert measurements
    measurements_insert_path = project_dir / 'database/insert/measurements.sql'
    measurements_insert_sql = load_sql(measurements_insert_path)
    measurements_to_insert = prepare_measurements(data)

    for measurement in measurements_to_insert:
        cur.execute(measurements_insert_sql, measurement)
        measurement_id = cur.fetchone()[0]
        conn.commit()

        # Prepare and insert trend data
        trends_insert_path = project_dir / 'database/insert/trends.sql'
        trends_insert_sql = load_sql(trends_insert_path)
        trends_to_insert = prepare_trends(data, measurement_id)

        for trend in trends_to_insert:
            cur.execute(trends_insert_sql, trend)
            conn.commit()

    cur.close()
    conn.close()


def authenticate_and_fetch_data(email, password):
    token = login(email, password)
    patient_data = get_patient_connections(token)
    patient_id = patient_data['data'][0]["patientId"]
    return get_cgm_data(token, patient_id)


def handle_timestamps(data):
    timestamp_format = '%m/%d/%Y %I:%M:%S %p'
    for item in data:
        item['Timestamp'] = datetime.strptime(
            item['Timestamp'], timestamp_format)
        item['FactoryTimestamp'] = datetime.strptime(
            item['FactoryTimestamp'], timestamp_format)


def main():
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    cgm_data = authenticate_and_fetch_data(email, password)
    graph_data = cgm_data['data']['graphData']
    glucose_measurement = cgm_data['data']['connection']['glucoseMeasurement']

    append_json(glucose_measurement, 'data/rt_data.json')
    live_data = load_from_json('data/rt_data.json')

    graph_data.extend(live_data)
    handle_timestamps(graph_data)

    database_pipe(graph_data)


if __name__ == "__main__":
    # schedule.every(1).minutes.do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    main()
