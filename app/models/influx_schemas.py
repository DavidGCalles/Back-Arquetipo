"""This module defines the Marshmallow schemas for InfluxDB operations."""
from marshmallow import Schema, fields

class InfluxWriteSchema(Schema):
    """Schema for validating data to be written to InfluxDB."""
    measurement = fields.Str(required=True, metadata={'description': "The name of the measurement."})
    tags = fields.Dict(keys=fields.Str(), values=fields.Str(), required=True, metadata={'description': "A dictionary of tags."})
    fields = fields.Dict(keys=fields.Str(), values=fields.Raw(), required=True, metadata={'description': "A dictionary of fields (float, int, str, or bool)."})

class InfluxQueryArgsSchema(Schema):
    """Schema for validating query arguments for InfluxDB."""
    bucket = fields.Str(required=True, metadata={'description': "The name of the bucket to query."})
    measurement = fields.Str(required=True, metadata={'description': "The measurement to query."})
    start_range = fields.Str(required=True, metadata={'description': "The start of the time range (e.g., '-1h', '-7d')."})
    stop_range = fields.Str(metadata={'description': "The end of the time range (optional, defaults to now)."})

class InfluxRecordSchema(Schema):
    """A generic schema for a single record returned from an InfluxDB query."""
    class Meta:
        # InfluxDB records have a variable structure (tags), so we include unknown fields.
        unknown = 'INCLUDE'
