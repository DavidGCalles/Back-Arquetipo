from w1thermsensor import W1ThermSensor
from config import LOGGER
from time import sleep

class DeviceController:
    def __init__(self, data:dict):
        self.data = data
        self.sensor_instance = self.determine_device()
        LOGGER.info(f"Sensor instance: {self.sensor_instance}")
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
            instances= W1ThermSensor.get_available_sensors()
            #one line, filter the proper instance by id with bus_id
            proper_instance = next((x for x in instances if x.id == self.data["bus_id"]), None)
            return proper_instance
