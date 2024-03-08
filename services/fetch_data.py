from __future__ import annotations

import logging
import time
from datetime import datetime

import requests

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


def login(email, password, retries=3, delay=60*2):
    """Log in to LibreLinkUp and retrieve JWT token."""
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
            token = data.get('data', []).get("authTicket", []).get("token", [])
            logging.info(
                f"Successfully fetched data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            return token
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429 and attempt < retries:
                logging.info(
                    f"Rate limit exceeded, waiting {delay} seconds before retrying...")
                time.sleep(delay)
                continue
            raise


def get_patient_connections(token):
    """Retrieve patient connections from LibreLinkUp."""
    endpoint = "/llu/connections"
    headers = {**HEADERS, 'Authorization': f"Bearer {token}"}

    response = requests.get(BASE_URL + endpoint, headers=headers)
    response.raise_for_status()
    return response.json()


def get_cgm_data(token, patient_id):
    """Retrieve CGM data for a specific patient from LibreLinkUp."""
    endpoint = f"/llu/connections/{patient_id}/graph"
    headers = {**HEADERS, 'Authorization': f"Bearer {token}"}

    response = requests.get(BASE_URL + endpoint, headers=headers)
    response.raise_for_status()
    return response.json()


def authenticate_and_fetch_data(email, password):
    token = login(email, password)
    patient_data = get_patient_connections(token)
    patient_id = patient_data['data'][0]["patientId"]
    return get_cgm_data(token, patient_id)
