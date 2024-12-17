from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify
from app.dao.generic_dao import BaseDAO
from app.models.demo_schemas import ItemSchema, UpdateItemSchema, SuccessResponseSchema, MessageResponseSchema

# Blueprint
crud_bp = Blueprint('crud', __name__, description="Generic CRUD operations for items.")

# DAO
crud_dao = BaseDAO()

# Class-Based View
@crud_bp.route('/demo_crud')
class GenericCRUD(MethodView):
    @crud_bp.response(200, ItemSchema(many=True), description="Data is successfully retrieved.")
    @crud_bp.doc(summary="Retrieve all items", description="Fetch all items from the database.")
    def get(self):
        """
        GET method: Retrieve all items.
        """
        data = crud_dao.generic_get_all()
        return jsonify(data), 200

    @crud_bp.arguments(ItemSchema)
    @crud_bp.response(201, MessageResponseSchema, description="New item successfully inserted.")
    @crud_bp.response(503, MessageResponseSchema, description="Error inserting the item.")
    @crud_bp.doc(summary="Insert new item", description="Insert a new item into the database.")
    def post(self, new_data):
        """
        POST method: Insert new item.
        """
        result = crud_dao.generic_insert(new_data)
        if result:
            return {"message": "New item inserted"}, 201
        return {"message": "There was a problem inserting the item"}, 503

    @crud_bp.arguments(UpdateItemSchema)
    @crud_bp.response(200, SuccessResponseSchema, description="Item successfully updated.")
    @crud_bp.response(400, SuccessResponseSchema, description="Error updating the item.")
    @crud_bp.doc(summary="Update an item", description="Update an existing item using its ID.")
    def patch(self, update_data):
        """
        PATCH method: Update existing item.
        """
        item_id = update_data.pop("id", None)
        if not item_id:
            return {"success": False}, 400
        result = crud_dao.generic_update("id", update_data)
        if result:
            return {"success": True}, 200
        return {"success": False}, 400

    @crud_bp.arguments(UpdateItemSchema)
    @crud_bp.response(200, MessageResponseSchema, description="Item successfully deleted.")
    @crud_bp.response(503, MessageResponseSchema, description="Error deleting the item.")
    @crud_bp.doc(summary="Delete an item", description="Delete an item by its ID.")
    def delete(self, delete_data):
        """
        DELETE method: Delete item by ID.
        """
        item_id = delete_data.get("id")
        if crud_dao.generic_delete("id", item_id):
            return {"message": "Record deleted successfully"}, 200
        return {"message": "Record cannot be deleted"}, 503