from __future__ import annotations

import os
import time

from services.fetch_data import get_cgm_data
from services.fetch_data import get_patient_connections
from services.fetch_data import login
from utils.file_utils import append_json
from utils.file_utils import load_from_json
from utils.file_utils import save_to_json
from utils.file_utils import save_to_parquet


def authenticate_and_fetch_data(email, password):
    token = login(email, password)
    patient_data = get_patient_connections(token)
    patient_id = patient_data['data'][0]["patientId"]
    return get_cgm_data(token, patient_id)


def main():
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    cgm_data = authenticate_and_fetch_data(email, password)
    save_to_json(cgm_data, 'data/response.json')

    graph_data = cgm_data['data']['graphData']
    glucose_measurement = cgm_data['data']['connection']['glucoseMeasurement']
    # save_to_json([glucose_measurement], 'data/rt_data.json')   # only for initialising the file

    append_json(glucose_measurement, 'data/rt_data.json')
    live_data = load_from_json('data/rt_data.json')

    graph_data.extend(live_data)
    save_to_json(graph_data, 'data/combined_data.json')

    keys_to_remove = ['TrendMessage', 'TrendArrow', 'FactoryTimestamp']
    processed_data = [{k: v for k, v in item.items() if k not in keys_to_remove}
                      for item in graph_data]

    save_to_parquet(processed_data, 'data/combined_data.parquet')


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60*2)
