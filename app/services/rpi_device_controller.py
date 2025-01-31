from w1thermsensor import W1ThermSensor

class DeviceController:
    def __init__(self, data:dict):
        self.data = data
        self.sensor_instance = self.determine_device()
    def read_device(self):
        if self.sensor_instance is not None and isinstance(self.sensor_instance, W1ThermSensor):
            return self.sensor_instance.get_temperature("celsius")
    def write_device(self, state:str):
        pass
    def determine_device(self):
        if self.data["model"] == "D18B20":
            return W1ThermSensor(self.data["pin_number"])
