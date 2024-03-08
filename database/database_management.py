from __future__ import annotations

import logging

import psycopg2.pool
from sqlalchemy import create_engine

from database.utils_db.db_ops import prepare_measurements
from utils.setup_env import setup_project_env
project_dir, config, setup_logs, db_config = setup_project_env()


class DatabaseManagement:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.engine, self.conn = self.create_my_engine()
        self.pgsql_pool = self.create_my_pool()

    def load_sql(self, path):
        with open(path, 'r') as file:
            return file.read()

    def create_my_pool(self):
        """Initialize connection pool"""
        pgsql_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10,
            user=self.config["user"],
            password=self.config["password"],
            host=self.config["host"],
            port=self.config["port"],
            database=self.config["database"])
        return pgsql_pool

    def create_my_engine(self):
        """Get the database engine."""
        engine = create_engine(
            f'postgresql+psycopg2://{self.config["user"]}:{self.config["password"]}@{self.config["host"]}:{self.config["port"]}/{self.config["database"]}')
        conn = psycopg2.connect(
            f'dbname={self.config["database"]} user={self.config["user"]} host={self.config["host"]} password={self.config["password"]}')
        return engine, conn

    def insert_to_db(self, data):
        """Insert data into the database."""
        conn = self.pgsql_pool.getconn()

        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SET search_path TO libre_link")

                # Prepare and insert measurements
                measurements_insert_path = project_dir / 'database/insert/measurements.sql'
                measurements_insert_sql = self.load_sql(
                    measurements_insert_path)
                measurements_to_insert = prepare_measurements(data)

                for measurement in measurements_to_insert:
                    cur.execute(measurements_insert_sql, measurement)
                conn.commit()
                self.logger.info("Data inserted successfully.")
            except (Exception, psycopg2.DatabaseError) as error:
                conn.rollback()
                self.logger.error(f"Failed to insert data: {error}")
            finally:
                cur.close()
                self.pgsql_pool.putconn(conn)

    def close_pool(self):
        """Close the connection pool on exit."""
        self.pgsql_pool.closeall()
        self.logger.info("Connection pool closed.")
