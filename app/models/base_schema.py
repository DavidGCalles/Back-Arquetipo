from marshmallow import Schema

class BaseSchema(Schema):
    """
    BaseSchema: Class to manage the schema of the base model.
    """
    @staticmethod
    def from_array_to_json(values):
        keys = BaseSchema().fields.keys()
        return dict(zip(keys, values))
    
