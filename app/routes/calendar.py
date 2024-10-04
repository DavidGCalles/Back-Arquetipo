"""This blueprint holds every endpoint related to basic crud operations, used for demo purposes"""
from flask import Blueprint, jsonify, request
from app.dao.generic_dao import BaseDAO

calendar_bp = Blueprint('calendar', __name__)

crud_dao = BaseDAO()

@calendar_bp.route('/calendar', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def calendar_methods():
    """
    Generic CRUD operations for handling items.

    ---
    methods:
        GET:
            description: Retrieve all items.
            responses:
                200:
                    description: Data is successfully retrieved.
                    schema:
                        type: object
                        properties:
                            data:
                                type: object
                                description: An object containing all items.
                400:
                    description: No data retrieved or error in fetching data.

        POST:
            description: Insert a new item.
            responses:
                200:
                    description: New item is successfully inserted.
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: "New Row inserted"
                503:
                    description: Error in inserting the item.
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: "There was a problem inserting row"
        PATCH:
            description: Update an existing item.
            responses:
                200:
                    description: Item is successfully updated.
                    schema:
                        type: object
                        properties:
                            success:
                                type: boolean
                                example: true
                400:
                    description: No ID provided or error in updating item.
                    schema:
                        type: object
                        properties:
                            success:
                                type: boolean
                                example: false
        DELETE:
            description: Delete an existing item.
            responses:
                200:
                    description: Item is successfully deleted.
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: "Record deleted successfully"
                503:
                    description: Unable to delete the item.
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: "Record cannot be deleted"
    """
    if request.method == "GET":
        
        data = crud_dao.generic_get_all()
        return jsonify({"data": data}),200
    elif request.method == "POST":
        json_data = request.json
        result = crud_dao.generic_insert(json_data)
        if result is not None:
            return jsonify({"message": "New Row inserted"}), 201
        else:
            return jsonify({"message": "There was a problem inserting row"}), 503
    elif request.method == "PATCH":
        json_data = request.json
        id_request = json_data.get("id", None)
        if id_request is not None:
            result = crud_dao.generic_update("id",json_data)
            if result:
                return jsonify(True), 200
        else:
            return jsonify(False), 400
    elif request.method == "DELETE":
        id_request = request.json.get("id")
        if crud_dao.generic_delete("id",id_request):
            return jsonify({"message": "Record deleted succesfully"}), 200
        else:
            return jsonify({"message": "Record cant be deleted"}), 503
