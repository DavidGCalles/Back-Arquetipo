"""
Raspberry Pi Blueprint
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify
from app.models.demo_schemas import MessageResponseSchema
from app.models.rpi_schemas import DeviceSchema
from app.dao.rpi_dao import DeviceDAO
from app.services.rpi_device_controller import DeviceController
from config import LOGGER, Config
import requests

# Blueprint
rpi_device_bp = Blueprint('rpi_device', __name__, description="Blueprint dedicated to Raspberry Pi Device operations.")

rpi_host = Config.RPI_MIDDLEWARE_SETTINGS["RPI_CONTROLLER_HOST"]
rpi_port = Config.RPI_MIDDLEWARE_SETTINGS["RPI_CONTROLLER_PORT"]
base_url = f"http://{rpi_host}:{rpi_port}"

@rpi_device_bp.route("/rpi/device")
class DeviceCollection(MethodView):
    """
    DeviceCollection: Class to manage all device items.
    """
    @rpi_device_bp.response(200, DeviceSchema, description="Device data successfully retrieved.")
    @rpi_device_bp.doc(summary="Retrieve device data", description="Retrieve data for a specific device ID.")
    def get(self):
        """
        GET method: Retrieve data for a specific device ID.
        """
        try:
            url = f"{base_url}/rpi/device/"
            LOGGER.info("URL generated: %s", url)
            result = requests.get(url=url, timeout=10)
            return jsonify(result.json()), result.status_code
        except KeyError:
            return jsonify({"error": "Device ID not initialized or host not reachable"}), 404
    @rpi_device_bp.arguments(DeviceSchema)
    @rpi_device_bp.response(201, MessageResponseSchema, description="New device successfully inserted.")
    @rpi_device_bp.doc(summary="Insert new device", description="Insert a new device into the database.")
    def post(self, request):
        """
        POST method: Insert data for a new device.
        """
        url = f"{base_url}/rpi/device"
        LOGGER.info("Request data: %s", request)
        result = requests.post(url=url, json=request, timeout=10)
        if result.status_code == 201:
            return {"message": "New device inserted"}, 201
        return {"message": "There was a problem inserting the device"}, 503

@rpi_device_bp.route("/rpi/device/<int:device_id>")
class DeviceCrud(MethodView):
    @rpi_device_bp.response(200, DeviceSchema, description="Device data successfully retrieved.")
    @rpi_device_bp.doc(summary="Retrieve device data", description="Retrieve data for a specific device ID.")
    def get(self, device_id:int):
        """
        GET method: Retrieve data for a specific device ID.
        """
        url = f"{base_url}/rpi/device/{device_id}"
        LOGGER.info("URL generated: %s", url)
        result = requests.get(url=url, timeout=10)
        return jsonify(result.json()), result.status_code
    
    @rpi_device_bp.response(200, MessageResponseSchema, description="Device data successfully deleted.")
    @rpi_device_bp.doc(summary="Delete device data", description="Delete data for a specific device ID.")
    def delete(self, device_id):
        """
        DELETE method: Delete data for a specific device ID.
        """
        url = f"{base_url}/rpi/device/{device_id}"
        LOGGER.info("URL generated: %s", url)
        result = requests.delete(url=url, timeout=10)
        return jsonify(result.json()), result.status_code
        
    @rpi_device_bp.arguments(DeviceSchema)
    @rpi_device_bp.response(200, MessageResponseSchema, description="Device data successfully updated.")
    @rpi_device_bp.doc(summary="Update device data", description="Update data for a specific device ID.")
    def patch(self,request, device_id:int):
        """
        PATCH method: Update data for a specific device ID.
        """
        url = f"{base_url}/rpi/device/{device_id}"
        LOGGER.info("Request data: %s", request)
        result = requests.patch(url=url, json=request, timeout=10)
        return jsonify(result.json()), result.status_code

@rpi_device_bp.route("/rpi/device/<int:device_id>/read")
class DeviceRead(MethodView):
    @rpi_device_bp.response(200, description="Device data successfully read.")
    @rpi_device_bp.response(404, description="Device not found.")
    @rpi_device_bp.doc(summary="Read device data", description="Read data for a specific device ID.")
    def get(self, device_id:int):
        """
        GET method: Read data for a specific device ID.
        """
        url = f"{base_url}/rpi/device/{device_id}/read"
        LOGGER.info("URL generated: %s", url)
        result = requests.get(url=url, timeout=10)
        return jsonify(result.json()), result.status_code
    