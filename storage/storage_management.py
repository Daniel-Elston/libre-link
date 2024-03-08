from __future__ import annotations

import json

import pandas as pd


class StorageManagement:
    def __init__(self, base_path="data/"):
        self.base_path = base_path

    def save_to_json(self, data, filename):
        path = self.base_path + filename
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)

    def load_from_json(self, filename):
        path = self.base_path + filename
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def append_json(self, data, filename):
        path = self.base_path + filename
        try:
            with open(path, 'r') as file:
                file_data = json.load(file)
        except FileNotFoundError:
            file_data = []

        file_data.append(data)
        with open(path, 'w') as file:
            json.dump(file_data, file, indent=4)

    def save_to_parquet(self, data, filename):
        path = self.base_path + filename
        df = pd.json_normalize(data)
        df.to_parquet(path, index=False)

    def load_from_parquet(self, filename):
        path = self.base_path + filename
        return self._load_dataframe_from_parquet(path)

    @staticmethod
    def _load_dataframe_from_parquet(path):
        try:
            return pd.read_parquet(path)
        except FileNotFoundError:
            return pd.DataFrame()
