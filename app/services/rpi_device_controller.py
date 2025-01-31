from w1thermsensor import W1ThermSensor

class DeviceController:
    def __init__(self, data:dict):
        self.data = data
        self.sensor_instance = self.determine_device()
    def read_device(self):
        if self.sensor_instance is not None and isinstance(self.sensor_instance, W1ThermSensor):
            result = self.sensor_instance.get_temperature("celsius")
            return result
    def write_device(self, state:str):
        pass
    def determine_device(self):
        if self.data["model"] == "DS18B20":
            instances= W1ThermSensor.get_available_sensors()
            proper_instance = next((x for x in instances if x.id == self.data["bus_id"]), None)
            if not proper_instance:
                raise NameError(f"Device not found in {len(instances)} devices")
            return proper_instance
