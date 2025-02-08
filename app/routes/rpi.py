"""
Raspberry Pi Blueprint
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify
from app.models.demo_schemas import ItemSchema
from config import LOGGER

# Blueprint
rpi_bp = Blueprint('rpi', __name__, description="Blueprint dedicated to Raspberry Pi operations.")

@rpi_bp.route('/rpi')
class RpiCollection(MethodView):
    """
    RpiCollection: Class to manage all RPi items."""
    @rpi_bp.response(200, ItemSchema(many=True), description="Data successfully retrieved.")
    @rpi_bp.doc(summary="Retrieve device data", description="Fetch RPi data, like servername, ip, etc.")
    def get(self):
        """
        GET method: Retrieve all items.
        """
        LOGGER.info("GET RPI method called")
        return jsonify(True), 200