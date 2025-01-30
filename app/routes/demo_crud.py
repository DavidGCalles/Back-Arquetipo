from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify, request
from app.dao.generic_dao import BaseDAO
from app.models.demo_schemas import ItemSchema, UpdateItemSchema, SuccessResponseSchema, MessageResponseSchema, SearchItemSchema
from config import LOGGER

# Blueprint
crud_bp = Blueprint('crud', __name__, description="CRUD operations for items.")

# DAO
crud_dao = BaseDAO()

# Operations for the collection (/demo_crud)
@crud_bp.route('/demo_crud')
class ItemCollection(MethodView):
    @crud_bp.response(200, ItemSchema(many=True), description="Data successfully retrieved.")
    @crud_bp.doc(summary="Retrieve all items", description="Fetch all items from the database.")
    def get(self):
        """
        GET method: Retrieve all items.
        """
        data = crud_dao.generic_get_all()
        if data:
            data = [ItemSchema().from_array_to_json(item) for item in data]
        return jsonify(data), 200

    @crud_bp.arguments(ItemSchema)
    @crud_bp.response(201, MessageResponseSchema, description="New item successfully inserted.")
    @crud_bp.response(503, MessageResponseSchema, description="Error inserting the item.")
    @crud_bp.doc(summary="Insert new item", description="Insert a new item into the database.")
    def post(self, new_data):
        """
        POST method: Insert a new item.
        """
        result = crud_dao.generic_insert(new_data)
        if result:
            return {"message": "New item inserted"}, 201
        return {"message": "There was a problem inserting the item"}, 503

# Operations for a single resource (/demo_crud/item/<id>)
@crud_bp.route('/demo_crud/item/<int:item_id>')
class ItemResource(MethodView):
    @crud_bp.response(200, ItemSchema, description="Item successfully retrieved.")
    @crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @crud_bp.doc(summary="Retrieve an item", description="Fetch an item by its ID.")
    def get(self, item_id):
        """
        GET method: Retrieve an item by ID.
        """
        item = crud_dao.generic_get_by_field("id", item_id)
        if item:
            return jsonify(ItemSchema().from_array_to_json(item)), 200
        return {"message": "Item not found"}, 404

    @crud_bp.arguments(UpdateItemSchema)
    @crud_bp.response(200, SuccessResponseSchema, description="Item successfully updated.")
    @crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @crud_bp.doc(summary="Update an item", description="Update an existing item by its ID.")
    def patch(self, update_data, item_id):
        """
        PATCH method: Update an item by ID.
        """
        result = crud_dao.generic_update("id", {"id": item_id, **update_data})
        if result:
            return {"success": True}, 200
        return {"message": "Item not found"}, 404

    @crud_bp.arguments(ItemSchema)
    @crud_bp.response(200, SuccessResponseSchema, description="Item successfully replaced.")
    @crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @crud_bp.doc(summary="Replace an item", description="Completely replace an item by its ID.")
    def put(self, new_data, item_id):
        """
        PUT method: Replace an item by ID.
        """
        LOGGER.info(f"Replacing item with ID: {item_id}")
        result = crud_dao.generic_replace({"id": item_id, **new_data})
        if result: 
            return {"success": True}, 200
        return {"message": "Item not found"}, 404

    @crud_bp.response(200, MessageResponseSchema, description="Item successfully deleted.")
    @crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @crud_bp.doc(summary="Delete an item", description="Delete an item by its ID.")
    def delete(self, item_id):
        """
        DELETE method: Delete an item by ID.
        """
        if crud_dao.generic_delete("id", item_id):
            return {"message": "Record deleted successfully"}, 200
        return {"message": "Item not found or cannot be deleted"}, 404
    
@crud_bp.route('/demo_crud/search')
class ItemSearch(MethodView):
    @crud_bp.response(200, ItemSchema(many=True), description="Items successfully retrieved.")
    @crud_bp.response(400, MessageResponseSchema, description="Invalid search parameters.")
    @crud_bp.arguments(SearchItemSchema, location="query")
    @crud_bp.doc(
        summary="Search items", 
        description="Search for items based on query parameters. Query parameters can include 'name', 'category', 'price_min', and 'price_max'."
    )
    def get(self, args):
        """
        GET method: Search items based on query parameters.

        Query parameters:
        - name: Name of the item to search for (optional)
        - category: Category of the item (optional)
        - price_min: Minimum price of the item (optional)
        - price_max: Maximum price of the item (optional)
        """
        query_params = {key: value for key, value in args.items() if value is not None}

        if not query_params:
            return {"message": "No search parameters provided"}, 400

        results = crud_dao.generic_search(query_params, True)
        if results:
            results = [ItemSchema().from_array_to_json(item) for item in results]
        return jsonify(results), 200
