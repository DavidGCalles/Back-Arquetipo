"""
demo_schemas: Module to manage the schemas of the demo application.
"""
from marshmallow import Schema, fields

class ItemSchema(Schema):
    """
    ItemSchema: Class to manage the schema of the items.
    """
    id = fields.Int(required=False, description="ID of the item")
    name = fields.Str(required=True, description="Name of the item")
    description = fields.Str(required=False, description="Description of the item")

class UpdateItemSchema(Schema):
    """
    UpdateItemSchema: Class to manage the schema of the items to update.
    """
    id = fields.Int(required=True, description="ID of the item to update")
    name = fields.Str(required=False, description="Updated name")
    description = fields.Str(required=False, description="Updated description")

class SearchItemSchema(Schema):
    """
    SearchItemSchema: Class to manage the schema of the items to search.
    """
    name = fields.Str(required=False)
    id = fields.Int(required=False)
    description = fields.Str(required=False, description="Updated description")

class SuccessResponseSchema(Schema):
    """
    SuccessResponseSchema: Class to manage the schema of the success response.
    """
    success = fields.Bool(description="Indicates whether the operation was successful")

class MessageResponseSchema(Schema):
    """
    MessageResponseSchema: Class to manage the schema of the message response.
    """
    message = fields.Str(description="Response message")