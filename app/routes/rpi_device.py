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
from config import LOGGER

# Blueprint
rpi_device_bp = Blueprint('rpi_device', __name__, description="Blueprint dedicated to Raspberry Pi Device operations.")

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
            return jsonify(DeviceDAO().get_all_devices()), 200
        except KeyError:
            return jsonify({"error": "Device ID not initialized"}), 404
    @rpi_device_bp.arguments(DeviceSchema)
    @rpi_device_bp.response(201, MessageResponseSchema, description="New device successfully inserted.")
    @rpi_device_bp.doc(summary="Insert new device", description="Insert a new device into the database.")
    def post(self, request):
        """
        POST method: Insert data for a new device.
        """
        request.pop("device_id", None)  # Remove device_id from request
        result = DeviceDAO().insert_device(request)
        if result:
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
        try:
            return jsonify(DeviceDAO().get_device(device_id)), 200
        except KeyError:
            return jsonify({"error": "Device ID not initialized"}), 404
    @rpi_device_bp.response(200, MessageResponseSchema, description="Device data successfully deleted.")
    @rpi_device_bp.doc(summary="Delete device data", description="Delete data for a specific device ID.")
    def delete(self, device_id):
        """
        DELETE method: Delete data for a specific device ID.
        """
        result = DeviceDAO().delete_device(device_id)
        if result:
            return {"message": "Device successfully deleted"}, 200
        return {"message": "Device not found"}, 404
    @rpi_device_bp.arguments(DeviceSchema)
    @rpi_device_bp.response(200, MessageResponseSchema, description="Device data successfully updated.")
    @rpi_device_bp.doc(summary="Update device data", description="Update data for a specific device ID.")
    def patch(self,request, device_id:int):
        """
        PATCH method: Update data for a specific device ID.
        """
        request.pop("device_id", None)
        result = DeviceDAO().update_device(device_id, request)
        if result:
            return {"success": True}, 200
        return {"message": "Device not found"}, 404

@rpi_device_bp.route("/rpi/device/<int:device_id>/read")
class DeviceRead(MethodView):
    @rpi_device_bp.response(200, description="Device data successfully read.")
    @rpi_device_bp.response(404, description="Device not found.")
    @rpi_device_bp.doc(summary="Read device data", description="Read data for a specific device ID.")
    def get(self, device_id:int):
        """
        GET method: Read data for a specific device ID.
        """
        try:
            device = DeviceDAO().get_device(device_id)
            if device:
                controller = DeviceController(device)
                value = controller.read_device()
                DeviceDAO().update_device(device_id, {"value": value})
                return jsonify(value), 200
            else:
                raise KeyError("Device not found")
        except KeyError as e:
            return jsonify({"message": "Device not found", "detail":e}), 404
        except NameError as e:
            return jsonify({"message": "Device not found", "detail": e}), 404