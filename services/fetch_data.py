from __future__ import annotations

import logging
import time
from datetime import datetime

import dotenv
import requests

from utils.setup_env import setup_project_env

# Load environment variables
dotenv.load_dotenv()

# Setup Logging
project_dir, config, setup_logs = setup_project_env()

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

# Function to log in and retrieve JWT token


def login(email, password, retries=3, delay=60*2):
    endpoint = "/llu/auth/login"
    payload = {
        "email": email,
        "password": password
    }

    for attempt in range(retries+1):
        try:
            response = requests.post(
                BASE_URL + endpoint, headers=HEADERS, json=payload)
            response.raise_for_status()
            data = response.json()
            # print(data)
            token = data.get('data', []).get("authTicket", []).get("token", [])
            # print(token)
            logging.info(
                f"Successful run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            return token
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429 and attempt < retries:
                logging.info(
                    f"Rate limit exceeded, waiting {delay} seconds before retrying...")
                time.sleep(delay)
                continue
            raise

# Function to get connections of patients


def get_patient_connections(token):
    endpoint = "/llu/connections"
    headers = {**HEADERS, 'Authorization': f"Bearer {token}"}

    response = requests.get(BASE_URL + endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to retrieve CGM data for a specific patient


def get_cgm_data(token, patient_id):
    endpoint = f"/llu/connections/{patient_id}/graph"
    headers = {**HEADERS, 'Authorization': f"Bearer {token}"}

    response = requests.get(BASE_URL + endpoint, headers=headers)
    response.raise_for_status()
    return response.json()
