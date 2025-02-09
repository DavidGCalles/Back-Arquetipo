"""
Raspberry Pi Blueprint
"""
import requests
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify, request
from app.models.demo_schemas import MessageResponseSchema
from app.models.rpi_schemas import PinSchema, PinControlSchema
from config import LOGGER, Config

# Blueprint
rpi_pin_bp = Blueprint('rpi_pin', __name__, description="Blueprint dedicated to Raspberry Pi PIN operations.")

# Extracted variables
rpi_host = Config.RPI_MIDDLEWARE_SETTINGS["RPI_CONTROLLER_HOST"]
rpi_port = Config.RPI_MIDDLEWARE_SETTINGS["RPI_CONTROLLER_PORT"]
base_url = f"http://{rpi_host}:{rpi_port}"

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
        url = f"{base_url}/rpi/pin"
        LOGGER.info("URL generated: %s", url)
        result = requests.get(url=url, timeout=10)
        return jsonify(result.json()), 200

    @rpi_pin_bp.arguments(PinSchema)
    @rpi_pin_bp.response(201, MessageResponseSchema, description="New pin successfully inserted.")
    @rpi_pin_bp.doc(summary="Insert new pin", description="Insert a new pin into the database.")
    def post(self, request_data):
        """
        POST method: Insert data for a new pin.
        """
        url = f"{base_url}/rpi/pin"
        LOGGER.info("Request data: %s", request_data)
        result = requests.post(url=url, json=request_data, timeout=10)
        if result.status_code == 201:
            return {"message": "New pin inserted"}, 201
        return {"message": "There was a problem inserting the pin"}, 503

@rpi_pin_bp.route("/rpi/pin/set_up_from_db")
class PinSetup(MethodView):
    @rpi_pin_bp.response(200, PinSchema, description="Pin data successfully retrieved and set up.")
    @rpi_pin_bp.doc(summary="Retrieve the pins from db and set them up", description="Retrieve the pins from db and set them up")
    def get(self):
        url = f"{base_url}/rpi/pin/set_up_from_db"
        LOGGER.info("URL generated: %s", url)
        result = requests.get(url=url, timeout=10)
        return jsonify(result.json()), result.status_code

@rpi_pin_bp.route("/rpi/pin/<int:pin_number>")
class PinCrud(MethodView):
    """
    PinCrud: Class to manage CRUD operations for a specific pin item.
    """
    @rpi_pin_bp.response(200, PinSchema, description="Pin data successfully retrieved.")
    @rpi_pin_bp.doc(summary="Retrieve pin data", description="Retrieve data for a specific pin number.")
    def get(self, pin_number: int):
        """
        GET method: Retrieve data for a specific pin number.
        """
        url = f"{base_url}/rpi/pin/{pin_number}"
        LOGGER.info("URL generated: %s", url)
        result = requests.get(url=url, timeout=10)
        return jsonify(result.json()), result.status_code

    @rpi_pin_bp.arguments(PinSchema)
    @rpi_pin_bp.response(200, MessageResponseSchema, description="Pin data successfully updated.")
    @rpi_pin_bp.doc(summary="Update pin data", description="Update data for a specific pin number.")
    def patch(self, request_data, pin_number: int):
        """
        PATCH method: Update data for a specific pin number.
        """
        url = f"{base_url}/rpi/pin/{pin_number}"
        LOGGER.info("Request data: %s", request_data)
        result = requests.patch(url=url, json=request_data, timeout=10)
        return jsonify(result.json()), result.status_code

    @rpi_pin_bp.response(200, MessageResponseSchema, description="Pin data successfully deleted.")
    @rpi_pin_bp.doc(summary="Delete pin data", description="Delete data for a specific pin number.")
    def delete(self, pin_number):
        """
        DELETE method: Delete data for a specific pin number.
        """
        url = f"{base_url}/rpi/pin/{pin_number}"
        LOGGER.info("URL generated: %s", url)
        result = requests.delete(url=url, timeout=10)
        return jsonify(result.json()), result.status_code

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
    def post(self, request_data):
        """
        POST method: Control a specific pin number. Pin needs to be registered as OUTPUT TO WORK
        """
        url = f"{base_url}/rpi/pin/control"
        LOGGER.info("Request data: %s", request_data)
        result = requests.post(url=url, json=request_data, timeout=10)
        return jsonify(result.json()), result.status_code