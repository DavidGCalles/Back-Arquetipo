from app.services.db import DBManager
from app.dao.generic_dao import BaseDAO
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
        result = self.generic_update("pin_number", fields)
        if result:
            return True
        return False

    def get_all_pins(self) -> list[dict[str, str]]: 
        return self.generic_get_all()

    def get_pin(self, pin_number: int) -> dict[str, str]: 
        result = self.generic_get_by_field("pin_number", pin_number)
        if result:
            return result
        return {}
    
    def delete_pin(self, pin_number: int):
        try:
            self.generic_delete("pin_number", pin_number)
            return True
        except Exception as e:
            LOGGER.error(f"Error deleting pin: {e}")
            return False



class DeviceDAO:
    def __init__(self):
        self.db_manager = DBManager()
        self.db_manager.reset_db_settings("sqlite-rpi")
        self.connection = self.db_manager.get_db_connection()
        self.table = "devices"

    def insert_device(self, device_info: dict): #Este sería generico
        try:
            columns = ', '.join(device_info.keys())
            placeholders = ', '.join(['?' for _ in device_info])
            query = f"INSERT INTO devices ({columns}) VALUES ({placeholders});"
            
            self.connection.execute(query, tuple(device_info.values()))
            self.connection.commit()
            return True
        except Exception as e:
            LOGGER.error(f"Error inserting device: {e}")
            return False

    def update_device(self, device_id: int, data: dict) -> bool: #Generico. Se puede quedar y configurar el diccionario
        try:
            updates = []
            params = []

            for key, value in data.items():
                updates.append(f"{key} = ?")
                params.append(value)

            params.append(device_id)
            query = f"""
            UPDATE devices
            SET {', '.join(updates)}
            WHERE device_id = ?;
            """
            self.connection.execute(query, params)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def get_all_devices(self) -> list[dict[str, str]]: #Generico
        query = "SELECT * FROM devices;"
        cursor = self.connection.execute(query)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_device(self, device_id: int) -> dict[str, str]: #Generico
        query = "SELECT * FROM devices WHERE device_id = ?;"
        cursor = self.connection.execute(query, (device_id,))
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, cursor.fetchone()))

    def delete_device(self, device_id: int): #Generico
        try:
            self.connection.execute("DELETE FROM devices WHERE device_id = ?;", (device_id,))
            self.connection.commit()
            return True
        except Exception as e:
            LOGGER.error(f"Error deleting device: {e}")
            return False