"""This module abstracts neccesary DB configuration and connections made"""
# app/db.py
from pathlib import Path
import os
import sqlite3
import mysql.connector
from mysql.connector import Error
from config import Config, LOGGER

class DBManager:
    def __init__(self):
        self.db_configs = Config.DATABASE_CONFIGURATIONS
        self.project_root = Path(__file__).resolve().parent.parent

    def get_db_connection(self, db_name: str):
        """Creates and return a db connection with the parameters given in config class"""
        if db_name not in self.db_configs:
            LOGGER.error("Database configuration '%s' not found.", db_name)
            return None

        db_settings = self.db_configs[db_name]
        db_type = "sqlite" if "sqlite" in db_name else "mysql" if "mysql" in db_name else None

        LOGGER.debug("Conectando a la base de datos %s", db_name)
        if db_type == "sqlite":
            try:
                connection = sqlite3.connect(db_settings["DB_HOST"])
                return connection
            except Error as e:
                LOGGER.error("Error connecting to SQLite3 (%s): %s", db_name, e)
                return None
        elif db_type == "mysql":
            try:
                connection = mysql.connector.connect(
                    host=db_settings["DB_HOST"],
                    port=db_settings["DB_PORT"],
                    database=db_settings["DB_NAME"],
                    user=db_settings["DB_USER"],
                    password=db_settings["DB_PASSWORD"],
                    charset='utf8mb4',  # Explicitly set charset
                    collation='utf8mb4_general_ci'  # Explicitly set collation
                )
                return connection
            except Error as e:
                LOGGER.error("Error connecting to MySQL (%s): %s", db_name, e)
                return None
        else:
            LOGGER.error("Database type for '%s' not supported.", db_name)
            return None