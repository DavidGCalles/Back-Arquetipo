"""Main Blueprint, made for checking services"""
from flask import jsonify, current_app, send_from_directory
from flask_smorest import Blueprint
from app.services.db import DBManager
from config import LOGGER
import os

main_bp = Blueprint('checks', __name__)

@main_bp.route('/', methods=['GET'])
@main_bp.response(200, {"message": {"type": "string"}}, description="Successful response indicating the server is reachable.")
def index():
    """
    Makes a ping request to the server to test basic connectivity.
    """
    LOGGER.warning("This the root")
    if os.environ("RPI_MODULE"):
        return send_from_directory(os.path.join(current_app.root_path, 'static'), 'index.html')
    else:
        return jsonify({"message": "Flask API"}), 404


@main_bp.route('/ping', methods=['GET'])
@main_bp.response(200, {"message": {"type": "string"}}, description="Successful response indicating the server is reachable.")
def ping():
    """
    Makes a ping request to the server to test basic connectivity.
    """
    LOGGER.warning("This is a ping")
    return jsonify({"message": "pong"})


@main_bp.route('/test_db', methods=["GET"])
@main_bp.response(200, {"message": {"type": "string"}}, description="Database is connected.")
@main_bp.response(503, {"message": {"type": "string"}}, description="Database is not connected.")
def test_db():
    """
    Tests the database connection and returns the status.
    """
    conn = DBManager().get_db_connection()
    if conn is not None:
        return jsonify({"message": "Database Correctly Connected"}), 200
    else:
        return jsonify({"message": "Database Not Connected"}), 503
    
@main_bp.route('/check_blueprints', methods=["GET"])
@main_bp.response(200, {"message": {"type": "string"}, "blueprints": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "url_prefix": {"type": "string"}}}}}, description="Blueprints are correctly registered.")
@main_bp.response(503, {"message": {"type": "string"}}, description="Blueprints are not correctly registered.")
def check_blueprints():
    """
    Tests if the blueprints are correctly registered and returns the status.
    """
    if current_app.blueprints:
        blueprints_info = [{"name": name, "url_prefix": blueprint.url_prefix} for name, blueprint in current_app.blueprints.items()]
        return jsonify({"message": "Blueprints are correctly registered", "blueprints": blueprints_info}), 200
    else:
        return jsonify({"message": "Blueprints are not correctly registered"}), 503