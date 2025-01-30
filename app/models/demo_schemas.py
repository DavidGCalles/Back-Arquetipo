"""
demo_schemas: Module to manage the schemas of the demo application.
"""
from marshmallow import Schema, fields
from app.models.base_schema import BaseSchema

class ItemSchema(BaseSchema):
    """
    ItemSchema: Class to manage the schema of the items.
    """
    id = fields.Int(required=False, metadata={"description": "ID of the item"})
    name = fields.Str(required=True, metadata={"description": "Name of the item"})
    description = fields.Str(required=False, metadata={"description": "Description of the item"})

class UpdateItemSchema(BaseSchema):
    """
    UpdateItemSchema: Class to manage the schema of the items to update.
    """
    id = fields.Int(required=True, metadata={"description": "ID of the item to update"})
    name = fields.Str(required=False, metadata={"description": "Updated name"})
    description = fields.Str(required=False, metadata={"description": "Updated description"})

class SearchItemSchema(BaseSchema):
    """
    SearchItemSchema: Class to manage the schema of the items to search.
    """
    name = fields.Str(required=False)
    id = fields.Int(required=False)
    description = fields.Str(required=False, metadata={"description": "Updated description"})


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