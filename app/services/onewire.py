from w1thermsensor import W1ThermSensor

class OneWire:
    def __init__(self, pin):
        self.pin = pin
    def scan(self):
        # Scan for all devices connected to the GPIO pin
        return W1ThermSensor.get_available_sensors()
    def get_by_id(self, device_id):
        # Get the sensor by its ID
        return W1ThermSensor(sensor_id=device_id)
    
W1ThermSensor(1).get_temperature("celsius")