from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from app.routes.main import main_bp
from app.routes.demo_crud import crud_bp
from app.services.db import DBManager
import os

def create_app():
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
        app.config['SWAGGER_UI_HOST'] = os.getenv("SWAGGER_UI_HOST")
    CORS(app, origins=["https://front-arquetipo-856517455627.europe-southwest1.run.app"],
         expose_headers=['Content-Type'], 
         supports_credentials=True)
    api = Api(app)

    api.register_blueprint(main_bp)
    api.register_blueprint(crud_bp)
    DBManager().check_coherence()
    return app
