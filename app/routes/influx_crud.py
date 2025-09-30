"""This module provides a demo CRUD for InfluxDB, integrated with Flask-Smorest."""
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify
from app.dao.influx_dao import InfluxDAO
from app.models.influx_schemas import InfluxWriteSchema, InfluxQueryArgsSchema, InfluxRecordSchema
from app.models.demo_schemas import MessageResponseSchema
from config import LOGGER

influx_crud_bp = Blueprint(
    'influx_crud', 
    __name__, 
    url_prefix='/influx', 
    description="CRUD operations for InfluxDB."
)

@influx_crud_bp.route('/')
class InfluxDBResource(MethodView):

    @influx_crud_bp.arguments(InfluxWriteSchema)
    @influx_crud_bp.response(201, MessageResponseSchema, description="Data successfully written to InfluxDB.")
    @influx_crud_bp.response(500, MessageResponseSchema, description="Error writing to InfluxDB.")
    @influx_crud_bp.doc(summary="Write data to InfluxDB", description="Writes a single data point to the specified measurement.")
    def post(self, new_data):
        """
        POST method: Write a data point to InfluxDB.
        """
        try:
            dao = InfluxDAO()
            success = dao.write(
                measurement=new_data['measurement'],
                tags=new_data['tags'],
                fields=new_data['fields']
            )
            if success:
                return {"message": "Data written successfully"}, 201
            else:
                return {"message": "Failed to write data to InfluxDB"}, 500
        except Exception as e:
            LOGGER.error(f"Error writing to InfluxDB: {e}")
            return {"message": "An unexpected error occurred"}, 500

    @influx_crud_bp.arguments(InfluxQueryArgsSchema, location="query")
    @influx_crud_bp.response(200, InfluxRecordSchema(many=True), description="Data successfully retrieved from InfluxDB.")
    @influx_crud_bp.response(500, MessageResponseSchema, description="Error querying InfluxDB.")
    @influx_crud_bp.doc(summary="Query data from InfluxDB", description="Queries data from a specified bucket within the last hour.")
    def get(self, args):
        """
        GET method: Query data from InfluxDB.
        """
        try:
            dao = InfluxDAO()
            results = dao.query(
                bucket=args['bucket'],
                measurement=args['measurement'],
                start_range=args['start_range'],
                stop_range=args.get('stop_range') # Optional
            )

            if results is not None:
                return jsonify(results), 200
            else:
                return {"message": "Failed to query data from InfluxDB"}, 500
        except Exception as e:
            LOGGER.error(f"Error querying InfluxDB: {e}")
            return {"message": "An unexpected error occurred"}, 500
