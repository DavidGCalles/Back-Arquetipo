"""This module abstracts neccesary DB configuration and connections made"""
# app/db.py

import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    """Creates and return a db connection with the parameters given in config class"""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            charset='utf8mb4',  # Explicitly set charset
            collation='utf8mb4_general_ci'  # Explicitly set collation
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
