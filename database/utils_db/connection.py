from __future__ import annotations

import os

import psycopg2
from sqlalchemy import create_engine


def create_my_engine(config):
    """
    Get the database engine.

    config: Configuration dictionary.
    """
    conf = {
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
        'database': os.getenv('POSTGRES_DB')
    }
    engine = create_engine(
        f'postgresql+psycopg2://{conf["user"]}:{conf["password"]}@{conf["host"]}:{conf["port"]}/{conf["database"]}')
    conn = psycopg2.connect(
        f'dbname={conf["database"]} user={conf["user"]} host={conf["host"]} password={conf["password"]}')

    return engine, conn
