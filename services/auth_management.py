from __future__ import annotations

import logging
import os
import time
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


class AuthenticationManagement():
    def __init__(self, config):
        self.config = config
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.token = self.login()

    def login(self, retries=3, delay=60*2):
        """Log in to LibreLinkUp and retrieve JWT token."""
        endpoint = "/llu/auth/login"
        payload = {
            "email": self.email,
            "password": self.password
        }

        for attempt in range(retries+1):
            try:
                response = requests.post(
                    BASE_URL + endpoint, headers=HEADERS, json=payload)
                response.raise_for_status()
                data = response.json()
                token = data.get('data', []).get(
                    "authTicket", []).get("token", [])
                self.logger.info(
                    f"Successfully logged in at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                return token
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429 and attempt < retries:
                    self.logger.warning(
                        f"Rate limit exceeded, waiting {delay} seconds before retrying...")
                    time.sleep(delay)
                    continue
                raise

    def get_patient_connections(self):
        """Retrieve patient connections from LibreLinkUp."""
        endpoint = "/llu/connections"
        headers = {**HEADERS, 'Authorization': f"Bearer {self.token}"}

        response = requests.get(BASE_URL + endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_patient_id(self):
        patient_data = self.get_patient_connections()
        patient_id = patient_data['data'][0]["patientId"]
        return patient_id
