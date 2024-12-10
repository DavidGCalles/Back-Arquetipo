from flask import jsonify, request
from flask_smorest import Blueprint
from app.dao.generic_dao import BaseDAO

crud_bp = Blueprint('crud', __name__)

crud_dao = BaseDAO()

@crud_bp.route('/crud', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@crud_bp.doc(description="Generic CRUD operations for handling items.")
# GET method - no parameters (retrieving all items)
@crud_bp.response(200, {"data": {"type": "object"}}, description="Data is successfully retrieved.")
@crud_bp.response(400, {"message": {"type": "string"}}, description="No data retrieved or error in fetching data.")
# POST method - requires JSON body with item data
@crud_bp.response(201, {"message": {"type": "string"}}, description="New item is successfully inserted.")
@crud_bp.response(503, {"message": {"type": "string"}}, description="Error in inserting the item.")
# PATCH method - requires ID and data to update
@crud_bp.response(200, {"success": {"type": "boolean"}}, description="Item is successfully updated.")
@crud_bp.response(400, {"success": {"type": "boolean"}}, description="No ID provided or error in updating item.")
# DELETE method - requires ID to delete
@crud_bp.response(200, {"message": {"type": "string"}}, description="Item is successfully deleted.")
@crud_bp.response(503, {"message": {"type": "string"}}, description="Unable to delete the item.")
def generic_crud():
    """
    Handles generic CRUD operations for items.
    """
    if request.method == "GET":
        # Retrieve all items (no parameters)
        data = crud_dao.generic_get_all()
        return jsonify({"data": data}), 200

    elif request.method == "POST":
        # Insert new item (expects JSON body)
        json_data = request.json
        result = crud_dao.generic_insert(json_data)
        if result is not None:
            return jsonify({"message": "New Row inserted"}), 201
        else:
            return jsonify({"message": "There was a problem inserting row"}), 503

    elif request.method == "PATCH":
        # Update existing item (expects ID and JSON body with data)
        json_data = request.json
        id_request = json_data.get("id", None)
        if id_request is not None:
            result = crud_dao.generic_update("id", json_data)
            if result:
                return jsonify({"success": True}), 200
        return jsonify({"success": False}), 400

    elif request.method == "DELETE":
        # Delete item (expects ID in request body)
        id_request = request.json.get("id")
        if crud_dao.generic_delete("id", id_request):
            return jsonify({"message": "Record deleted successfully"}), 200
        else:
            return jsonify({"message": "Record cannot be deleted"}), 503
