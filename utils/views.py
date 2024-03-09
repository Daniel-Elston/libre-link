from __future__ import annotations

import pandas as pd
import plotly.express as px

from database.database_management import DatabaseManagement
from utils.setup_env import setup_project_env
project_dir, config, setup_logs, db_config = setup_project_env()


def inspect():
    """Inspect most recent data in the database"""
    db_manager = DatabaseManagement(db_config)
    data = db_manager.fetch_data()
    df = pd.json_normalize(data)
    df_descending = df.sort_values(by='timestamp', ascending=False)
    print(df_descending.head())
    return df


def plots(df):
    fig = px.line(df, x="timestamp", y="value")
    fig.show()


def pipeline():
    df = inspect()
    plots(df)


if __name__ == '__main__':
    pipeline()
