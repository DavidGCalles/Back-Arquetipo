"""
This module initializes the Flask application, configures the API and CORS settings, 
registers the blueprints, and checks the database coherence.
"""
import os
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from app.routes.main import main_bp
from app.routes.demo_crud import crud_bp
#from app.routes.rpi import rpi_bp
#from app.routes.rpi_pin import rpi_pin_bp
#from app.routes.rpi_device import rpi_device_bp
from app.services.db import DBManager
from config import Config


def create_app():
    """Initializes the Flask application, configures the API and CORS settings,
    registers the blueprints, and checks the database coherence."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config["API_TITLE"] = "Flask API"
    app.config["API_VERSION"] = "1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_JSON_PATH"] = "swagger.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    if os.getenv("SWAGGER_HOST"):
        app.config['SWAGGER_UI_HOST'] = os.getenv("SWAGGER_HOST")
    origins_allowed = []
    if Config.FLASK_ENV is None or Config.FLASK_ENV == "development":
        origins_allowed.append("http://localhost:8080")
    else:
        origins_allowed.append("https://front-arquetipo-856517455627.europe-southwest1.run.app")
    CORS(app, origins=origins_allowed,
         expose_headers=['Content-Type'],
         supports_credentials=True)
    api = Api(app)

    api.register_blueprint(main_bp)
    api.register_blueprint(crud_bp)
    if os.getenv("RPI_MODULE"):
        #api.register_blueprint(rpi_bp)
        #api.register_blueprint(rpi_pin_bp)
        #api.register_blueprint(rpi_device_bp)
        sqlite_manager = DBManager()
        sqlite_manager.reset_db_settings("sqlite-rpi")
        sqlite_manager.check_coherence()
    DBManager().check_coherence()
    return app
