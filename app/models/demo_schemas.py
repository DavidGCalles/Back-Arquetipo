from marshmallow import Schema, fields

class ItemSchema(Schema):
    id = fields.Int(required=False, description="ID of the item")
    name = fields.Str(required=True, description="Name of the item")
    description = fields.Str(required=False, description="Description of the item")

class UpdateItemSchema(Schema):
    id = fields.Int(required=True, description="ID of the item to update")
    name = fields.Str(required=False, description="Updated name")
    description = fields.Str(required=False, description="Updated description")

class SearchItemSchema(Schema):
    name = fields.Str(required=False)
    id = fields.Int(required=False)
    description = fields.Str(required=False, description="Updated description")

class SuccessResponseSchema(Schema):
    success = fields.Bool(description="Indicates whether the operation was successful")

class MessageResponseSchema(Schema):
    message = fields.Str(description="Response message")