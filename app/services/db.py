"""This module abstracts neccesary DB configuration and connections made"""
# app/db.py
import os
import sqlite3
import mysql.connector
from mysql.connector import Error
from config import Config, LOGGER

def get_db_connection():
    """Creates and return a db connection with the parameters given in config class"""
    db_type = os.getenv("DATABASE_TYPE", "sqlite")
    db_settings = Config.DB_TYPES[db_type]
    if db_type == "sqlite":
        try:
            connection = sqlite3.connect(db_settings["DB_HOST"])
        except Error as e:
            LOGGER.error("Error connecting to SQLite3: %s",e)
            return None
    elif db_type == "mysql":
        try:
            connection = mysql.connector.connect(
                host=db_settings["DB_HOST"],
                port=db_settings["DB_PORT"],
                database=db_settings["DB_NAME"],
                user=db_settings["DB_USER"],
                password=["DB_PASSWORD"],
                charset='utf8mb4',  # Explicitly set charset
                collation='utf8mb4_general_ci'  # Explicitly set collation
            )
            return connection
        except Error as e:
            LOGGER.error("Error connecting to MySQL: %s",e)
            return None
    else:
        LOGGER.error("Database type %s not supported.", db_type)
        return None
    