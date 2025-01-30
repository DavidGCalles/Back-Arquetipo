from marshmallow import Schema

class BaseSchema(Schema):
    """
    BaseSchema: Class to manage the schema of the base model.
    """
    def from_array_to_json(self, values):
        keys = self.fields.keys()
        return dict(zip(keys, values))
    
