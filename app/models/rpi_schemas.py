#Pin and device schemas are defined in rpi_schemas.py.

from marshmallow import Schema, fields

class PinSchema(Schema):
    """
    PinSchema: Class to manage the schema of the pins.
    """
    pin_number = fields.Int(required=True, metadata={"description": "Pin number"})
    name = fields.Str(required=True, metadata={"description": "Pin name"})
    mode = fields.Str(required=True, validate=lambda x: x in ['INPUT', 'OUTPUT'], metadata={"description": "Pin mode"})
    state = fields.Str(validate=lambda x: x in ['HIGH', 'LOW'], metadata={"description": "Pin state"})
    pull = fields.Str(validate=lambda x: x in ['PULL_UP', 'PULL_DOWN', 'NONE'], metadata={"description": "Pin pull"})
    protocol = fields.Str(validate=lambda x: x in ['I2C', 'SPI', 'UART', 'GPIO', 'ONEWIRE'], metadata={"description": "Pin protocol"})
    object_type = fields.Str(validate=lambda x: x in ['SENSOR', 'ACTUATOR', 'OTHER'], metadata={"description": "Pin object type"})

class DeviceSchema(Schema):
    """
    DeviceSchema: Class to manage the schema of the devices.
    """
    device_id = fields.Int(required=True, metadata={"description": "Device ID"})
    bus_id = fields.Str(metadata={"description": "Bus ID, for sensors or actuators connected to a bus"})
    name = fields.Str(required=True, metadata={"description": "Name of the device"})
    device_type = fields.Str(validate=lambda x: x in ['SENSOR', 'ACTUATOR'], metadata={"description": "Type of the device"})
    manufacturer = fields.Str(metadata={"description": "Manufacturer of the device"})
    model = fields.Str(metadata={"description": "Model of the device"})
    serial_number = fields.Str(metadata={"description": "Serial number of the device"})
    purchase_date = fields.Date(metadata={"description": "Purchase date of the device"})
    warranty_expiration = fields.Date(metadata={"description": "Warranty expiration date of the device"})
    location = fields.Str(metadata={"description": "Location of the device"})
    status = fields.Str(validate=lambda x: x in ['ACTIVE', 'INACTIVE', 'MAINTENANCE', 'RETIRED'], metadata={"description": "Status of the device"})
    pin_number = fields.Int(metadata={"description": "Pin number of the device"})
    range_min = fields.Int(metadata={"description": "Minimum range value of the device"})
    range_max = fields.Int(metadata={"description": "Maximum range value of the device"})
    measure_unit = fields.Str(metadata={"description": "Measurement unit of the device"})
    last_used = fields.DateTime(metadata={"description": "Last used date of the device"})
    value = fields.Str(metadata={"description": "Value of the device"})