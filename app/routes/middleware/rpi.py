"""
Raspberry Pi Blueprint
"""
import requests
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify
from app.models.demo_schemas import ItemSchema
from config import LOGGER, Config

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
        rpi_host = Config.RPI_MIDDLEWARE_SETTINGS["RPI_CONTROLLER_HOST"]
        rpi_port = Config.RPI_MIDDLEWARE_SETTINGS["RPI_CONTROLLER_PORT"]
        url = f"http://{rpi_host}:{rpi_port}/rpi"
        LOGGER.info("URL generada: %s", url)
        result = requests.get(url=url, timeout=10)
        return jsonify(result), 200