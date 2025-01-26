from w1thermsensor import W1ThermSensor

class OneWire:
    def __init__(self, pin):
        self.pin = pin
    def scan(self):
        # Scan for all devices connected to the GPIO pin
        return W1ThermSensor.get_available_sensors()