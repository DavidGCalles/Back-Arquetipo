from flask import Flask
from app import create_app
import os
from unittest.mock import patch

def test_create_app():
    app = create_app()
    assert isinstance(app, Flask)
    assert app.config["API_TITLE"] == "Flask API"
    assert app.config["API_VERSION"] == "1.0"
    assert app.config["OPENAPI_VERSION"] == "3.0.3"
    assert app.config["OPENAPI_JSON_PATH"] == "swagger.json"
    assert app.config["OPENAPI_URL_PREFIX"] == "/"
    assert app.config["OPENAPI_SWAGGER_UI_PATH"] == "/swagger"
    assert app.config["OPENAPI_SWAGGER_UI_URL"] == "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

def test_blueprints_registered():
    app = create_app()
    assert 'checks' in app.blueprints
    assert 'crud' in app.blueprints

@patch.dict(os.environ, {"RPI_MODULE": "1"})
def test_blueprints_registered_with_rpi_module():
    app = create_app()
    assert 'checks' in app.blueprints
    assert 'crud' in app.blueprints
    assert 'rpi' in app.blueprints

@patch.dict(os.environ, {"SWAGGER_HOST": "https://example.com"})
def test_swagger_host_config():
    app = create_app()
    assert app.config["SWAGGER_UI_HOST"] == "https://example.com"