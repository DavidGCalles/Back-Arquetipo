"""Main Blueprint, made for checking services"""
from flask import Blueprint, jsonify#, request
from app.services.db import get_db_connection

main_bp = Blueprint('main', __name__)

@main_bp.route('/ping', methods=['GET'])
def ping():
    """
    Ping endpoint to test the server.
    ---
    responses:
      200:
        description: Server is running
        schema:
          type: object
          properties:
            message:
              type: string
              example: pong
    """
    print("hello")
    return jsonify({"message": "pong"})

@main_bp.route('/test_db', methods=["GET"])
def test_db():
    """
    Endpoint to test the database connection.
    ---
    responses:
      200:
        description: Database is connected
        schema:
          type: object
          properties:
            message:
              type: string
              example: Database Correctly Connected
      503:
        description: Database is not connected
        schema:
          type: object
          properties:
            message:
              type: string
              example: Database Not Connected
    """
    conn = get_db_connection()
    if conn is not None:
        return jsonify({"message": "Database Correctly Connected"}),200
    else:
        return jsonify({"message": "Database Not Connected"}),503
