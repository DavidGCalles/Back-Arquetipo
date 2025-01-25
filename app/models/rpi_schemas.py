#Pin and device schemas are defined in rpi_schemas.py.

from marshmallow import Schema, fields

class PinSchema(Schema):
    """
    PinSchema: Class to manage the schema of the pins.
    """
    pin_number = fields.Int(required=True, metadata={"description": "Pin number"})
    pin_name = fields.Str(required=True, metadata={"description": "Pin name"})
    pin_type = fields.Str(required=True, metadata={"description": "Pin type"})
    pin_status = fields.Str(required=True, metadata={"description": "Pin status"})
    pin_value = fields.Str(required=True, metadata={"description": "Pin value"})
    pin_last_used = fields.Str(required=True, metadata={"description": "Pin last used"})
    pin_device = fields.Str(required=True, metadata={"description": "Pin device"})

class DeviceSchema(Schema):
    """
    DeviceSchema: Class to manage the schema of the devices.
    """
    device_id = fields.Int(required=True, metadata={"description": "Device ID"})
    name = fields.Str(required=True, metadata={"description": "Name of the device"})
    type = fields.Str(required=True, metadata={"description": "Type of the device"})
    manufacturer = fields.Str(required=True, metadata={"description": "Manufacturer of the device"})
    model = fields.Str(required=True, metadata={"description": "Model of the device"})
    serial_number = fields.Str(required=True, metadata={"description": "Serial number of the device"})
    purchase_date = fields.Str(required=True, metadata={"description": "Purchase date of the device"})
    warranty_expiration = fields.Str(required=True, metadata={"description": "Warranty expiration date of the device"})
    location = fields.Str(required=True, metadata={"description": "Location of the device"})
    status = fields.Str(required=True, metadata={"description": "Status of the device"})
    pin_number = fields.Int(required=True, metadata={"description": "Pin number of the device"})
    range_min = fields.Int(required=True, metadata={"description": "Minimum range value of the device"})
    range_max = fields.Int(required=True, metadata={"description": "Maximum range value of the device"})
    measure_unit = fields.Str(required=True, metadata={"description": "Measurement unit of the device"})
    last_used = fields.Str(required=True, metadata={"description": "Last used date of the device"})
    value = fields.Str(required=True, metadata={"description": "Value of the device"})