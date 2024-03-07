from __future__ import annotations

import json

import pandas as pd


def save_to_json(data, path):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)


def load_from_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def append_json(data, path):
    with open(path, 'r') as file:
        file_data = json.load(file)
    file_data.append(data)

    with open(path, 'w') as file:
        json.dump(file_data, file, indent=4)


def save_to_parquet(data, filepath):
    """Save data to a Parquet file."""
    df = pd.json_normalize(data)
    df.to_parquet(filepath, index=False)


def load_from_parquet(filepath):
    """Load data from a Parquet file."""
    try:
        df = pd.read_parquet(filepath)
        # return df.to_dict('records')
        return df
    except FileNotFoundError:
        return []
