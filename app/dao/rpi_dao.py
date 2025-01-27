from app.services.db import DBManager
from config import LOGGER

class GPIOControlDAO:
    def __init__(self):
        self.db_manager = DBManager()
        self.db_manager.reset_db_settings("sqlite-rpi")
        self.connection = self.db_manager.get_db_connection()
        self.table = "gpio_pins"

    def insert_or_ignore(self, data: dict):
        """
        Insert data into the database if it does not exist.
        Keys in data: pin_number, name, mode, state, pull, protocol, object_type.
        
        Args:
            data (dict): Data to insert.
        Returns:
            bool: True if the data was inserted, False otherwise.
        """
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join('?' * len(data))
            values = tuple(data.values())
            query = f"INSERT OR IGNORE INTO {self.table} ({columns}) VALUES ({placeholders})"
            self.connection.execute(query, values)
            self.connection.commit()
            return True
        except Exception as e:
            LOGGER.error("Error inserting data: %s", e)
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
        if not fields:
            return  # No updates to perform

        # Validate pin_number
        if not isinstance(pin_number, int):
            raise ValueError("pin_number must be an integer")

        # Validate immutable fields
        immutable_fields = ["pin_number"]
        for field in fields.keys():
            if field in immutable_fields:
                raise ValueError(f"Cannot update field '{field}'")

        set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
        params = list(fields.values()) + [pin_number]

        query = f"""
        UPDATE gpio_pins
        SET {set_clause}
        WHERE pin_number = ?;
        """
        self.connection.execute(query, params)
        self.connection.commit()
        return True

    def get_all_pins(self) -> list[dict[str, str]]:
        query = "SELECT * FROM gpio_pins;"
        cursor = self.connection.execute(query)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_pin(self, pin_number: int) -> dict[str, str]:
        query = "SELECT * FROM gpio_pins WHERE pin_number = ?;"
        cursor = self.connection.execute(query, (pin_number,))
        row = cursor.fetchone()
        if row is None:
            return {}
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, row))
    
    def delete_pin(self, pin_number: int):
        try:
            self.connection.execute("DELETE FROM gpio_pins WHERE pin_number = ?;", (pin_number,))
            self.connection.commit()
            return True
        except Exception as e:
            LOGGER.error(f"Error deleting pin: {e}")
            return False

    def delete_all(self):
        self.connection.execute("DELETE FROM gpio_pins;")
        self.connection.commit()

class DeviceDAO:
    def __init__(self):
        self.db_manager = DBManager()
        self.db_manager.reset_db_settings("sqlite-rpi")
        self.connection = self.db_manager.get_db_connection()
        self.table = "devices"

    def insert_device(self, device_info: dict):
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

    def update_device(self, device_id: int, data: dict) -> bool:
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

    def get_all_devices(self) -> list[dict[str, str]]:
        query = "SELECT * FROM devices;"
        cursor = self.connection.execute(query)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_device(self, device_id: int) -> dict[str, str]:
        query = "SELECT * FROM devices WHERE device_id = ?;"
        cursor = self.connection.execute(query, (device_id,))
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, cursor.fetchone()))

    def delete_device(self, device_id: int):
        try:
            self.connection.execute("DELETE FROM devices WHERE device_id = ?;", (device_id,))
            self.connection.commit()
            return True
        except Exception as e:
            LOGGER.error(f"Error deleting device: {e}")
            return False