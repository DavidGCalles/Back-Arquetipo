"""This module stores all config strings and details needed to run the app"""
import logging
import os
#from secrets_file import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

class Config:
    """Stores every config detail needed"""
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = 'your_secret_key'  # Replace with your actual secret key
    SWAGGER = {
        'title': 'Flask API',
        'uiversion': 3
    }
    DB_TYPES = {
        "sqlite": {
            "DB_HOST" : "inmemory.db"
        },
        "sqlite-rpi": {
            "DB_HOST": "rpi.db"
        },
        "mysql-docker": {
            "DB_HOST": 'db',
            "DB_PORT": '3306',
            "DB_NAME": 'your_database_name',
            "DB_USER": 'root',
            "DB_PASSWORD": 'toor'
        },
        "mysql": {
            "DB_HOST": 'localhost',
            "DB_PORT": '3306',
            "DB_NAME": 'your_database_name',
            "DB_USER": 'root',
            "DB_PASSWORD": 'toor'
        }
    }
    DDL_NAME = "models/ddl_sqlite.sql"
    DDL_RPI_NAME = "models/ddl_rpi.sql"
    DDL_MYSQL_NAME = "models/ddl_rpi.sql"
    GOOGLE_OAUTH = {
        "GOOGLE_CLIENT_ID" : "",#GOOGLE_CLIENT_ID,
        "GOOGLE_CLIENT_SECRET" :"",# GOOGLE_CLIENT_SECRET,
        "REDIRECT_URI" : 'http://localhost:5000/api/login/google_callback', ## Deberia estar parametrizado para no liarla en caso de otra configuracion
        "AUTH_URI" : 'https://accounts.google.com/o/oauth2/auth',
        "TOKEN_URI" : 'https://accounts.google.com/o/oauth2/token',
        "SCOPE" : ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar']
    }

# Setup logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)