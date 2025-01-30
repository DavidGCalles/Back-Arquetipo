from app.dao.generic_dao import BaseDAO
from app.models.rpi_schemas import PinSchema, DeviceSchema
from config import LOGGER

class GPIOControlDAO(BaseDAO):
    def __init__(self):
        super().__init__()
        self.db_manager.reset_db_settings("sqlite-rpi")
        self.table = "gpio_pins"

    def insert_or_ignore(self, data: dict):
        """
        Insert a new row in the database if it does not exist.

        Args:
            data (dict): Data to insert.
        Returns:
            bool: True if the data was inserted, False otherwise
        """
        result = self.generic_insert(data,True)
        if result:
            return True
        return False

    def update_pin(self, pin_number: int, fields: dict):
        """
        Update a pin in the database.
        Keys in fields: name, mode, state, pull, protocol, object_type.
        
        Args:
            pin_number (int): Pin number.
            fields (dict): Fields to update.
        Returns:
            bool: True if the data was updated, False otherwise.
        """
        fields["pin_number"] = pin_number
        result = self.generic_update("pin_number", fields)
        if result:
            return True
        return False

    def get_all_pins(self):
        result = self.generic_get_all()
        if result:
            LOGGER.info(f"Result: {result}")
            model_list = []
            for pin in result:
                model_list.append(PinSchema().from_array_to_json(pin))
            return model_list
        return []

    def get_pin(self, pin_number: int): 
        result = self.generic_get_by_field("pin_number", pin_number)
        if result:
            return PinSchema().from_array_to_json(result)
        return {}
    
    def delete_pin(self, pin_number: int):
        try:
            self.generic_delete("pin_number", pin_number)
            return True
        except Exception as e:
            LOGGER.error(f"Error deleting pin: {e}")
            return False

class DeviceDAO(BaseDAO):
    def __init__(self):
        super().__init__()
        self.db_manager.reset_db_settings("sqlite-rpi")
        self.table = "devices"

    def insert_device(self, device_info: dict):
        result = self.generic_insert(device_info)
        if result:
            return True
        return False

    def update_device(self, device_id: int, data: dict):
        data["device_id"] = device_id
        result = self.generic_update("device_id", data)
        if result:
            return True
        return False

    def get_all_devices(self):
        result = self.generic_get_all()
        if result:
            model_list = []
            for device in result:
                model_list.append(DeviceSchema().from_array_to_json(device))
            return model_list
        return []
    
    def get_device(self, device_id: int):
        result = self.generic_get_by_field("device_id", device_id)
        if result:
            return DeviceSchema().from_array_to_json(result)
        return {}

    def delete_device(self, device_id: int):
        try:
            self.generic_delete("device_id", device_id)
            return True
        except Exception as e:
            LOGGER.error(f"Error deleting device: {e}")
            return False
