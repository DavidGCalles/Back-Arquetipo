"""
Raspberry Pi Blueprint
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify
from app.models.demo_schemas import MessageResponseSchema
from app.models.rpi_schemas import PinSchema
from app.dao.rpi_dao import GPIOControlDAO
from config import LOGGER

# Blueprint
rpi_pin_bp = Blueprint('rpi_pin', __name__, description="Blueprint dedicated to Raspberry Pi PIN operations.")

@rpi_pin_bp.route("/rpi/pin")
class PinCollection(MethodView):
    """
    PinCollection: Class to manage all pin items.
    """
    @rpi_pin_bp.response(200, PinSchema, description="Pin data successfully retrieved.")
    @rpi_pin_bp.doc(summary="Retrieve pin data", description="Retrieve data for a specific pin number.")
    def get(self):
        """
        GET method: Retrieve data for a specific pin number.
        """
        try:
            return jsonify(GPIOControlDAO().get_all_pins()), 200
        except KeyError:
            return jsonify({"error": "Pin number not initialized"}), 404
    @rpi_pin_bp.arguments(PinSchema)
    @rpi_pin_bp.response(201, MessageResponseSchema, description="New pin successfully inserted.")
    @rpi_pin_bp.doc(summary="Insert new pin", description="Insert a new pin into the database.")
    def post(self,request):
        """
        POST method: Insert data for a new pin.
        """
        LOGGER.info("request dict: %s",request)
        result = GPIOControlDAO().insert_or_ignore(request)
        if result:
            return {"message": "New pin inserted"}, 201
        return {"message": "There was a problem inserting the pin"}, 503

@rpi_pin_bp.route("/rpi/pin/<int:pin_number>")
class PinCrud(MethodView):
    """
    PinCrud: Class to manage CRUD operations for a specific pin item.
    """
    @rpi_pin_bp.response(200, PinSchema, description="Pin data successfully retrieved.")
    @rpi_pin_bp.doc(summary="Retrieve pin data", description="Retrieve data for a specific pin number.")
    def get(self, pin_number:int):
        """
        GET method: Retrieve data for a specific pin number.
        """
        try:
            return jsonify(GPIOControlDAO().get_pin(pin_number)), 200
        except KeyError:
            return jsonify({"error": "Pin number not initialized"}), 404
    
    @rpi_pin_bp.arguments(PinSchema)
    @rpi_pin_bp.response(200, MessageResponseSchema, description="Pin data successfully updated.")
    @rpi_pin_bp.doc(summary="Update pin data", description="Update data for a specific pin number.")
    def patch(self, request, pin_number:int):
        """
        PATCH method: Update data for a specific pin number.
        """
        request.pop("pin_number", None)  # Remove pin_number from request
        result = GPIOControlDAO().update_pin(pin_number, request)
        if result:
            return {"success": True}, 200
        return {"message": "Pin not found"}, 404
    
    @rpi_pin_bp.response(200, MessageResponseSchema, description="Pin data successfully deleted.")
    @rpi_pin_bp.doc(summary="Delete pin data", description="Delete data for a specific pin number.")
    def delete(self, pin_number):
        """
        DELETE method: Delete data for a specific pin number.
        """
        pin_to_delete = GPIOControlDAO().get_pin(pin_number)
        if not pin_to_delete:
            return {"message": "Pin not found"}, 404
        result = GPIOControlDAO().delete_pin(pin_number)
        if result:
            return {"message": "Pin successfully deleted"}, 200
        return {"message": "Pin not found"}, 404
