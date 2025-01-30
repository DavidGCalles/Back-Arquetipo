"""
demo_schemas: Module to manage the schemas of the demo application.
"""
from marshmallow import Schema, fields

class ItemSchema(Schema):
    """
    ItemSchema: Class to manage the schema of the items.
    """
    id = fields.Int(required=False, metadata={"description": "ID of the item"})
    name = fields.Str(required=True, metadata={"description": "Name of the item"})
    description = fields.Str(required=False, metadata={"description": "Description of the item"})

    @staticmethod
    def from_array_to_json(values):
        keys = ItemSchema().fields.keys()
        return dict(zip(keys, values))

class UpdateItemSchema(Schema):
    """
    UpdateItemSchema: Class to manage the schema of the items to update.
    """
    id = fields.Int(required=True, metadata={"description": "ID of the item to update"})
    name = fields.Str(required=False, metadata={"description": "Updated name"})
    description = fields.Str(required=False, metadata={"description": "Updated description"})

    @staticmethod
    def from_array_to_json(values):
        keys = UpdateItemSchema().fields.keys()
        return dict(zip(keys, values))

class SearchItemSchema(Schema):
    """
    SearchItemSchema: Class to manage the schema of the items to search.
    """
    name = fields.Str(required=False)
    id = fields.Int(required=False)
    description = fields.Str(required=False, metadata={"description": "Updated description"})

    @staticmethod
    def from_array_to_json(values):
        keys = SearchItemSchema().fields.keys()
        return dict(zip(keys, values))

class SuccessResponseSchema(Schema):
    """
    SuccessResponseSchema: Class to manage the schema of the success response.
    """
    success = fields.Bool(metadata={"description": "Indicates whether the operation was successful"})

class MessageResponseSchema(Schema):
    """
    MessageResponseSchema: Class to manage the schema of the message response.
    """
    message = fields.Str(metadata={"description": "Response message"})