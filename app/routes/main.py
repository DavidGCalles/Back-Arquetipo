"""Main Blueprint, made for checking services"""
from flask import jsonify, current_app, send_from_directory
from flask.views import MethodView
from flask_smorest import Blueprint
from app.services.db import DBManager
from config import LOGGER
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', description="Admin and monitoring endpoints.")

@admin_bp.route('/', methods=['GET'])
@admin_bp.response(200, {"message": {"type": "string"}}, description="Successful response indicating the server is reachable.")
def index():
    """
    Serves static index in case of RPI module, 404 otherwise.
    """
    LOGGER.warning("This the root")
    if os.environ.get("RPI_MODULE"):
        return send_from_directory(os.path.join(current_app.root_path, 'static'), 'index.html')
    else:
        return jsonify({"message": "Flask API - RPI module not enabled"}), 404


@admin_bp.route('/ping', methods=['GET'])
@admin_bp.response(200, {"message": {"type": "string"}}, description="Successful response indicating the server is reachable.")
def ping():
    """
    Makes a ping request to the server to test basic connectivity.
    """
    LOGGER.warning("This is a ping")
    return jsonify({"message": "pong"})


@admin_bp.route('/test_db', methods=["GET"])
@admin_bp.response(200, {"message": {"type": "string"}}, description="Database is connected.")
@admin_bp.response(503, {"message": {"type": "string"}}, description="Database is not connected.")
def test_db():
    """
    Tests the database connection and returns the status.
    """
    conn = DBManager().get_db_connection("sqlite")
    if conn is not None:
        return jsonify({"message": "Database Correctly Connected"}), 200
    else:
        return jsonify({"message": "Database Not Connected"}), 503
    
@admin_bp.route('/check_blueprints', methods=["GET"])
@admin_bp.response(200, {"message": {"type": "string"}, "blueprints": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "url_prefix": {"type": "string"}}}}}, description="Blueprints are correctly registered.")
@admin_bp.response(503, {"message": {"type": "string"}}, description="Blueprints are not correctly registered.")
def check_blueprints():
    """
    Tests if the blueprints are correctly registered and returns the status.
    """
    if current_app.blueprints:
        blueprints_info = [{"name": name, "url_prefix": blueprint.url_prefix} for name, blueprint in current_app.blueprints.items()]
        return jsonify({"message": "Blueprints are correctly registered", "blueprints": blueprints_info}), 200
    else:
        return jsonify({"message": "Blueprints are not correctly registered"}), 503

@admin_bp.route('/init-db')
class InitDB(MethodView):
    @admin_bp.response(200, description="Databases initialized successfully.")
    @admin_bp.response(500, description="Error initializing databases.")
    @admin_bp.doc(summary="Initialize all configured databases", description="Executes the DDL scripts for all databases configured in the application.")
    def post(self):
        """
        POST method: Initialize all databases.
        """
        db_manager = DBManager()
        success = True
        for db_name in db_manager.db_configs:
            if not db_manager.initialize_database(db_name):
                success = False
        
        if success:
            return jsonify({"message": "All databases initialized successfully."}), 200
        else:
            return jsonify({"message": "An error occurred during database initialization."}), 500