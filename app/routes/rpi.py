"""
Raspberry Pi Blueprint
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify, request
from app.models.demo_schemas import ItemSchema, MessageResponseSchema
from app.models.rpi_schemas import PinSchema, DeviceSchema
from app.dao.rpi_dao import GPIOControlDAO, DeviceDAO
from config import Config, LOGGER


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

@rpi_bp.route("/rpi/pin")
class PinCollection(MethodView):
    """
    PinCollection: Class to manage all pin items.
    """
    @rpi_bp.response(200, PinSchema, description="Pin data successfully retrieved.")
    @rpi_bp.doc(summary="Retrieve pin data", description="Retrieve data for a specific pin number.")
    def get(self, pin_number:int):
        """
        GET method: Retrieve data for a specific pin number.
        """
        try:
            return jsonify(GPIOControlDAO().get_all_pins()), 200
        except KeyError:
            return jsonify({"error": "Pin number not initialized"}), 404
    @rpi_bp.arguments(PinSchema)
    @rpi_bp.response(201, MessageResponseSchema, description="New pin successfully inserted.")
    @rpi_bp.doc(summary="Insert new pin", description="Insert a new pin into the database.")
    def post(self):
        """
        POST method: Insert data for a new pin.
        """
        result = GPIOControlDAO().insert_or_ignore(request.json)
        if result:
            return {"message": "New pin inserted"}, 201
        return {"message": "There was a problem inserting the pin"}, 503

@rpi_bp.route("/rpi/pin/<int:pin_number>")
class PinCrud(MethodView):
    """
    PinCrud: Class to manage CRUD operations for a specific pin item.
    """
    @rpi_bp.response(200, PinSchema, description="Pin data successfully retrieved.")
    @rpi_bp.doc(summary="Retrieve pin data", description="Retrieve data for a specific pin number.")
    def get(self, pin_number:int):
        """
        GET method: Retrieve data for a specific pin number.
        """
        try:
            return jsonify(GPIOControlDAO().get_pin(pin_number)), 200
        except KeyError:
            return jsonify({"error": "Pin number not initialized"}), 404
    def patch(self, pin_number:int):
        """
        PATCH method: Update data for a specific pin number.
        """
        result = GPIOControlDAO().update_pin(pin_number, request.json)
        if result:
            return {"success": True}, 200
        return {"message": "Pin not found"}, 404
    
    def delete(self, pin_number):
        """
        DELETE method: Delete data for a specific pin number.
        """
        result = GPIOControlDAO().delete_pin(pin_number)
        if result:
            return {"message": "Pin successfully deleted"}, 200
        return {"message": "Pin not found"}, 404
        
        
@rpi_bp.route("/rpi/device/<int:device_id>")
class DeviceCrud(MethodView):
    @rpi_bp.response(200, DeviceSchema, description="Device data successfully retrieved.")
    @rpi_bp.doc(summary="Retrieve device data", description="Retrieve data for a specific device ID.")
    def get(self, device_id:int):
        """
        GET method: Retrieve data for a specific device ID.
        """
        try:
            return jsonify(True), 200
        except KeyError:
            return jsonify({"error": "Device ID not initialized"}), 404
    def put(self, device_id):
        """
        PUT method: Update data for a specific device ID.
        """
        pass
    def delete(self, device_id):
        """
        DELETE method: Delete data for a specific device ID.
        """
        pass
    def post(self):
        """
        POST method: Insert data for a new device.
        """
        pass
    def patch(self):
        """
        PATCH method: Update data for a specific device ID.
        """
        pass
