"""
Raspberry Pi Blueprint
"""
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify
from app.models.demo_schemas import MessageResponseSchema
from app.models.rpi_schemas import PinSchema, PinControlSchema
from app.dao.rpi_dao import GPIOControlDAO
from config import LOGGER
from rpi_cao import GPIOCAO

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

@rpi_pin_bp.route("/rpi/pin/set_up_from_db")
class PinSetup(MethodView):
    @rpi_pin_bp.response(200, PinSchema, description="Pin data successfully retrieved and set up.")
    @rpi_pin_bp.doc(summary="Retrieve the pins from db and set them up", description="Retrieve the pins from db and set them up")
    def get(self):
        pins_data = GPIOControlDAO().get_all_pins()
        try:
            for pin_dict in pins_data:
                GPIOCAO.setup_pin(pin_dict["pin_number"],
                                pin_dict["mode"],
                                pin_dict["pull"],
                                pin_dict["state"])
        except Exception as e:
            LOGGER.error("Problem mounting pins")
            return jsonify({"message": "Error setting up pins from db"}), 404
        return jsonify({"message": "All pins set up", "data": pins_data}), 200
            



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

@rpi_pin_bp.route("/rpi/pin/control")
class PinControl(MethodView):
    """
    PinControl: Class to manage control operations for a specific pin item.
    """
    @rpi_pin_bp.arguments(PinControlSchema)
    @rpi_pin_bp.response(200, MessageResponseSchema, description="Pin control operation successfully executed.")
    @rpi_pin_bp.response(404, MessageResponseSchema, description="Pin not registered")
    @rpi_pin_bp.response(404, MessageResponseSchema, description="Pin not configured as OUTPUT")
    @rpi_pin_bp.doc(summary="Control pin", description="Control a specific pin number.")
    def post(self, request):
        """
        POST method: Control a specific pin number. Pin needs to be registered as OUTPUT TO WORK
        """
        LOGGER.info("request dict: %s",request)
        pin_number = request["pin_number"]
        state = request["state"]
        pin_data = None
        try:
            pin_data = GPIOControlDAO().get_pin(pin_number)
        except IndexError as e:
            return {"message": "Pin not registered"},404

        if pin_data["mode"] != "OUTPUT":
            return {"message": "Pin not configured as OUTPUT"}, 404
        
        if pin_data["state"] == state:
            return {"message": f"Pin already in state: {state}"}, 200

        GPIOCAO.setup_pin(pin_number, "OUTPUT")
        if GPIOCAO.write_pin(pin_number, state):
            GPIOControlDAO().update_pin(pin_number, {"state": state})
            return {"message": "Pin controlled"}, 200
        return {"message": "Pin not found"}, 404