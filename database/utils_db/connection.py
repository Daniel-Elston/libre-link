from __future__ import annotations

import psycopg2
from sqlalchemy import create_engine


def create_my_engine(config):
    """Get the database engine."""
    engine = create_engine(
        f'postgresql+psycopg2://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/{config["database"]}')
    conn = psycopg2.connect(
        f'dbname={config["database"]} user={config["user"]} host={config["host"]} password={config["password"]}')

    return engine, conn


def create_my_pool(config):
    """Initialize connection pool"""
    pgsql_pool = psycopg2.pool.SimpleConnectionPool(
        1, 10,
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
        database=config["database"])
    return pgsql_pool
