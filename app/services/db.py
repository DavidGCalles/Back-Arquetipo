"""This module abstracts neccesary DB configuration and connections made"""
# app/db.py
from pathlib import Path
import os
import sqlite3
import mysql.connector
from mysql.connector import Error
from config import Config, LOGGER
from os import getcwd

class DBManager:
    def __init__(self):
        self.db_type = os.getenv("DATABASE_TYPE", "sqlite")
        self.db_settings = Config.DB_TYPES[self.db_type]
        self.project_root = Path(__file__).resolve().parent.parent
        LOGGER.error("Project root: %s", self.project_root)
    def check_coherence(self):
        LOGGER.info("Chequeando la coherencia de la base de datos %s", self.db_type)
        if self.db_type == "sqlite":
            try:
                conn = self.get_db_connection()
                cur = conn.cursor()
                ddl_path = self.project_root / Config.DDL_NAME
                LOGGER.info("Cargando ddl")
                LOGGER.error(getcwd())
                with open(ddl_path, 'r', encoding="UTF-8") as file:
                    sql_script = file.read()
                cur.executescript(sql_script)
                conn.commit()
                conn.close()
                LOGGER.info("Comprobación terminada")
                return True
            except Exception as e:
                LOGGER.error("Ha habido algun problema con la coherencia de la base de datos: %s",e)
                return False
            
    def get_db_connection(self):
        """Creates and return a db connection with the parameters given in config class"""
        if self.db_type == "sqlite":
            try:
                connection = sqlite3.connect(self.db_settings["DB_HOST"])
                return connection
            except Error as e:
                LOGGER.error("Error connecting to SQLite3: %s",e)
                return None
        elif self.db_type == "mysql":
            try:
                connection = mysql.connector.connect(
                    host=self.db_settings["DB_HOST"],
                    port=self.db_settings["DB_PORT"],
                    database=self.db_settings["DB_NAME"],
                    user=self.db_settings["DB_USER"],
                    password=self.db_settings["DB_PASSWORD"],
                    charset='utf8mb4',  # Explicitly set charset
                    collation='utf8mb4_general_ci'  # Explicitly set collation
                )
                return connection
            except Error as e:
                LOGGER.error("Error connecting to MySQL: %s",e)
                return None
        else:
            LOGGER.error("Database type %s not supported.", self.db_type)
            return None