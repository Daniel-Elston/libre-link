from __future__ import annotations

import os
from datetime import datetime

import requests

from utils.setup_env import setup_project_env
project_dir, config, setup_logs, db_config = setup_project_env()

# Constants
BASE_URL = "https://api.libreview.io"
HEADERS = {
    'accept-encoding': 'gzip',
    'cache-control': 'no-cache',
    'connection': 'Keep-Alive',
    'content-type': 'application/json',
    'product': 'llu.android',
    'version': '4.7'
}


class DataManagement:
    def __init__(self, config, token, patient_id):
        self.config = config
        self.token = token
        self.patient_id = patient_id
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.cgm_data = self.get_cgm_data(self.token, self.patient_id)

    def get_cgm_data(self, token, patient_id):
        """Retrieve CGM data for a specific patient from LibreLinkUp."""
        endpoint = f"/llu/connections/{patient_id}/graph"
        headers = {**HEADERS, 'Authorization': f"Bearer {token}"}

        response = requests.get(BASE_URL + endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_measurements(self):
        glucose_measurement = self.cgm_data['data']['connection']['glucoseMeasurement']
        return [glucose_measurement]

    def process_timestamps(self, data):
        """Convert timestamps to datetime objects."""
        timestamp_format = '%m/%d/%Y %I:%M:%S %p'
        for item in data:
            item['Timestamp'] = datetime.strptime(
                item['Timestamp'], timestamp_format)
            item['FactoryTimestamp'] = datetime.strptime(
                item['FactoryTimestamp'], timestamp_format)
