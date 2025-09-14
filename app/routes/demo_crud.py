from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify
from app.dao.generic_dao import BaseDAO
from app.models.demo_schemas import CreateItemSchema, ItemSchema, UpdateItemSchema, SuccessResponseSchema, MessageResponseSchema, SearchItemSchema
from config import LOGGER

# --- SQLite Blueprint ---
sqlite_crud_bp = Blueprint('sqlite_crud', __name__, url_prefix='/demo_crud/sqlite', description="CRUD operations for items on SQLite.")
sqlite_dao = BaseDAO("sqlite")

@sqlite_crud_bp.route('/')
class SqliteItemCollection(MethodView):
    @sqlite_crud_bp.response(200, ItemSchema(many=True), description="Data successfully retrieved.")
    @sqlite_crud_bp.doc(summary="Retrieve all items from SQLite", description="Fetch all items from the SQLite database.")
    def get(self):
        """
        GET method: Retrieve all items from SQLite.
        """
        data = sqlite_dao.generic_get_all()
        if data:
            data = [ItemSchema().from_array_to_json(item) for item in data]
        return jsonify(data), 200

    @sqlite_crud_bp.arguments(CreateItemSchema)
    @sqlite_crud_bp.response(201, MessageResponseSchema, description="New item successfully inserted.")
    @sqlite_crud_bp.response(503, MessageResponseSchema, description="Error inserting the item.")
    @sqlite_crud_bp.doc(summary="Insert new item into SQLite", description="Insert a new item into the SQLite database.")
    def post(self, new_data):
        """
        POST method: Insert a new item into SQLite.
        """
        result = sqlite_dao.generic_insert(new_data)
        if result:
            return {"message": "New item inserted"}, 201
        return {"message": "There was a problem inserting the item"}, 503

@sqlite_crud_bp.route('/item/<int:item_id>')
class SqliteItemResource(MethodView):
    @sqlite_crud_bp.response(200, ItemSchema, description="Item successfully retrieved.")
    @sqlite_crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @sqlite_crud_bp.doc(summary="Retrieve an item from SQLite", description="Fetch an item by its ID from the SQLite database.")
    def get(self, item_id):
        """
        GET method: Retrieve an item by ID from SQLite.
        """
        item = sqlite_dao.generic_get_by_field("id", item_id)
        if item:
            return jsonify(ItemSchema().from_array_to_json(item)), 200
        return {"message": "Item not found"}, 404

    @sqlite_crud_bp.arguments(UpdateItemSchema)
    @sqlite_crud_bp.response(200, SuccessResponseSchema, description="Item successfully updated.")
    @sqlite_crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @sqlite_crud_bp.doc(summary="Update an item in SQLite", description="Update an existing item by its ID in the SQLite database.")
    def patch(self, update_data, item_id):
        """
        PATCH method: Update an item by ID in SQLite.
        """
        result = sqlite_dao.generic_update("id", {"id": item_id, **update_data})
        if result:
            return {"success": True}, 200
        return {"message": "Item not found"}, 404

    @sqlite_crud_bp.arguments(ItemSchema)
    @sqlite_crud_bp.response(200, SuccessResponseSchema, description="Item successfully replaced.")
    @sqlite_crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @sqlite_crud_bp.doc(summary="Replace an item in SQLite", description="Completely replace an item by its ID in the SQLite database.")
    def put(self, new_data, item_id):
        """
        PUT method: Replace an item by ID in SQLite.
        """
        LOGGER.info(f"Replacing item with ID: {item_id}")
        result = sqlite_dao.generic_replace({"id": item_id, **new_data})
        if result:
            return {"success": True}, 200
        return {"message": "Item not found"}, 404

    @sqlite_crud_bp.response(200, MessageResponseSchema, description="Item successfully deleted.")
    @sqlite_crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @sqlite_crud_bp.doc(summary="Delete an item from SQLite", description="Delete an item by its ID from the SQLite database.")
    def delete(self, item_id):
        """
        DELETE method: Delete an item by ID from SQLite.
        """
        if sqlite_dao.generic_delete("id", item_id):
            return {"message": "Record deleted successfully"}, 200
        return {"message": "Item not found or cannot be deleted"}, 404

@sqlite_crud_bp.route('/search')
class SqliteItemSearch(MethodView):
    @sqlite_crud_bp.response(200, ItemSchema(many=True), description="Items successfully retrieved.")
    @sqlite_crud_bp.response(400, MessageResponseSchema, description="Invalid search parameters.")
    @sqlite_crud_bp.arguments(SearchItemSchema, location="query")
    @sqlite_crud_bp.doc(summary="Search items in SQLite", description="Search for items in SQLite based on query parameters.")
    def get(self, args):
        """
        GET method: Search items in SQLite based on query parameters.

        Query parameters:
        - name: Name of the item to search for (optional)
        - category: Category of the item (optional)
        - price_min: Minimum price of the item (optional)
        - price_max: Maximum price of the item (optional)
        """
        query_params = {key: value for key, value in args.items() if value is not None}

        if not query_params:
            return {"message": "No search parameters provided"}, 400

        results = sqlite_dao.generic_search(query_params, True)
        if results:
            results = [ItemSchema().from_array_to_json(item) for item in results]
        return jsonify(results), 200

# --- MySQL Blueprint ---
mysql_crud_bp = Blueprint('mysql_crud', __name__, url_prefix='/demo_crud/mysql', description="CRUD operations for items on MySQL.")
mysql_dao = BaseDAO("mysql-docker")

@mysql_crud_bp.route('/')
class MysqlItemCollection(MethodView):
    @mysql_crud_bp.response(200, ItemSchema(many=True), description="Data successfully retrieved.")
    @mysql_crud_bp.doc(summary="Retrieve all items from MySQL", description="Fetch all items from the MySQL database.")
    def get(self):
        """
        GET method: Retrieve all items from MySQL.
        """
        data = mysql_dao.generic_get_all()
        if data:
            data = [ItemSchema().from_array_to_json(item) for item in data]
        return jsonify(data), 200

    @mysql_crud_bp.arguments(CreateItemSchema)
    @mysql_crud_bp.response(201, MessageResponseSchema, description="New item successfully inserted.")
    @mysql_crud_bp.response(503, MessageResponseSchema, description="Error inserting the item.")
    @mysql_crud_bp.doc(summary="Insert new item into MySQL", description="Insert a new item into the MySQL database.")
    def post(self, new_data):
        """
        POST method: Insert a new item into MySQL.
        """
        result = mysql_dao.generic_insert(new_data)
        if result:
            return {"message": "New item inserted"}, 201
        return {"message": "There was a problem inserting the item"}, 503

@mysql_crud_bp.route('/item/<int:item_id>')
class MysqlItemResource(MethodView):
    @mysql_crud_bp.response(200, ItemSchema, description="Item successfully retrieved.")
    @mysql_crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @mysql_crud_bp.doc(summary="Retrieve an item from MySQL", description="Fetch an item by its ID from the MySQL database.")
    def get(self, item_id):
        """
        GET method: Retrieve an item by ID from MySQL.
        """
        item = mysql_dao.generic_get_by_field("id", item_id)
        if item:
            return jsonify(ItemSchema().from_array_to_json(item)), 200
        return {"message": "Item not found"}, 404

    @mysql_crud_bp.arguments(UpdateItemSchema)
    @mysql_crud_bp.response(200, SuccessResponseSchema, description="Item successfully updated.")
    @mysql_crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @mysql_crud_bp.doc(summary="Update an item in MySQL", description="Update an existing item by its ID in the MySQL database.")
    def patch(self, update_data, item_id):
        """
        PATCH method: Update an item by ID in MySQL.
        """
        result = mysql_dao.generic_update("id", {"id": item_id, **update_data})
        if result:
            return {"success": True}, 200
        return {"message": "Item not found"}, 404

    @mysql_crud_bp.arguments(ItemSchema)
    @mysql_crud_bp.response(200, SuccessResponseSchema, description="Item successfully replaced.")
    @mysql_crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @mysql_crud_bp.doc(summary="Replace an item in MySQL", description="Completely replace an item by its ID in the MySQL database.")
    def put(self, new_data, item_id):
        """
        PUT method: Replace an item by ID in MySQL.
        """
        LOGGER.info(f"Replacing item with ID: {item_id}")
        result = mysql_dao.generic_replace({"id": item_id, **new_data})
        if result:
            return {"success": True}, 200
        return {"message": "Item not found"}, 404

    @mysql_crud_bp.response(200, MessageResponseSchema, description="Item successfully deleted.")
    @mysql_crud_bp.response(404, MessageResponseSchema, description="Item not found.")
    @mysql_crud_bp.doc(summary="Delete an item from MySQL", description="Delete an item by its ID from the MySQL database.")
    def delete(self, item_id):
        """
        DELETE method: Delete an item by ID from MySQL.
        """
        if mysql_dao.generic_delete("id", item_id):
            return {"message": "Record deleted successfully"}, 200
        return {"message": "Item not found or cannot be deleted"}, 404

@mysql_crud_bp.route('/search')
class MysqlItemSearch(MethodView):
    @mysql_crud_bp.response(200, ItemSchema(many=True), description="Items successfully retrieved.")
    @mysql_crud_bp.response(400, MessageResponseSchema, description="Invalid search parameters.")
    @mysql_crud_bp.arguments(SearchItemSchema, location="query")
    @mysql_crud_bp.doc(summary="Search items in MySQL", description="Search for items in MySQL based on query parameters.")
    def get(self, args):
        """
        GET method: Search items in MySQL based on query parameters.

        Query parameters:
        - name: Name of the item to search for (optional)
        - category: Category of the item (optional)
        - price_min: Minimum price of the item (optional)
        - price_max: Maximum price of the item (optional)
        """
        query_params = {key: value for key, value in args.items() if value is not None}
        if not query_params:
            return {"message": "No search parameters provided"}, 400
        results = mysql_dao.generic_search(query_params, True)
        if results:
            results = [ItemSchema().from_array_to_json(item) for item in results]
        return jsonify(results), 200
