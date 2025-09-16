"""This module provides a demo CRUD for InfluxDB."""
from flask_smorest import Blueprint
from flask import request, jsonify
from app.dao.influx_dao import InfluxDAO
from config import LOGGER

influx_crud_bp = Blueprint('influx_crud', __name__, url_prefix='/api/influx', description="CRUD operations for InfluxDB.")

@influx_crud_bp.route('/write', methods=['POST'])
def write_influx_data():
    """
    Writes a sample data point to InfluxDB.
    Expects a JSON payload with 'measurement', 'tags', and 'fields'.
    Example:
    {
        "measurement": "system_stats",
        "tags": {"host": "server01"},
        "fields": {"cpu_load": 0.95, "memory_usage": 85}
    }
    """
    data = request.get_json()
    if not data or not all(k in data for k in ['measurement', 'tags', 'fields']):
        return jsonify({"error": "Missing required fields: measurement, tags, fields"}), 400

    try:
        dao = InfluxDAO()
        success = dao.write(
            measurement=data['measurement'],
            tags=data['tags'],
            fields=data['fields']
        )
        if success:
            return jsonify({"message": "Data written successfully"}), 201
        else:
            return jsonify({"error": "Failed to write data to InfluxDB"}), 500
    except Exception as e:
        LOGGER.error(f"Error writing to InfluxDB: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@influx_crud_bp.route('/query', methods=['GET'])
def query_influx_data():
    """
    Queries data from InfluxDB.
    Expects a 'bucket' query parameter.
    Example: /query?bucket=your_influx_bucket
    """
    bucket = request.args.get('bucket')
    if not bucket:
        return jsonify({"error": "Missing required query parameter: bucket"}), 400

    try:
        dao = InfluxDAO()
        # Simple query to get data from the last hour
        query = f'from(bucket:"{bucket}") |> range(start: -1h)'
        results = dao.query(query)

        if results is not None:
            return jsonify(results), 200
        else:
            return jsonify({"error": "Failed to query data from InfluxDB"}), 500
    except Exception as e:
        LOGGER.error(f"Error querying InfluxDB: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
