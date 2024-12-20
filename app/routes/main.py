"""Main Blueprint, made for checking services"""
from flask import jsonify
from flask_smorest import Blueprint
from app.services.db import DBManager
from config import LOGGER

main_bp = Blueprint('checks', __name__)

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
