from w1thermsensor import W1ThermSensor
from config import LOGGER

class DeviceController:
    def __init__(self, data:dict):
        self.data = data
        self.sensor_instance = self.determine_device()
    def read_device(self):
        if self.sensor_instance is not None and isinstance(self.sensor_instance, W1ThermSensor):
            result = self.sensor_instance.get_temperature("celsius")
            LOGGER.info(f"Temperature read: {result} and type: {type(result)}")
            return self.sensor_instance.get_temperature("celsius")
        return {}
    def write_device(self, state:str):
        pass
    def determine_device(self):
        if self.data["model"] == "D18B20":
            return W1ThermSensor(self.data["bus_id"])
