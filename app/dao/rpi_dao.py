from app.services.db import DBManager
from config import LOGGER

class GPIOControlDAO:
    def __init__(self):
        self.db_manager = DBManager()
        self.db_manager.reset_db_settings("sqlite-rpi")
        self.connection = DBManager().get_db_connection()
        self.table = "gpio_pins" 

    def insert_or_ignore(self, data: dict):
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join('?' * len(data))
            values = tuple(data.values())
            query = f"INSERT OR IGNORE INTO {self.table} ({columns}) VALUES ({placeholders})"
            self.connection.execute(query, values)
            self.connection.commit()
            return True
        except Exception as e:
            LOGGER.error(f"Error inserting data: {e}")
            return False

    def update_pin(self, pin_number: int, fields: dict):
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
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, cursor.fetchone()))
    
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
        self.connection = DBManager().get_db_connection()

    def insert_device(self, name: str, type: str, manufacturer: str, model: str, serial_number: str, purchase_date: str, warranty_expiration: str, location: str, status: str, pin_number: int, range_min: int, range_max: int, measure_unit: str, last_used: str, value: str):
        query = """
        INSERT INTO devices (name, type, manufacturer, model, serial_number, purchase_date, warranty_expiration, location, status, pin_number, range_min, range_max, measure_unit, last_used, value)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        self.connection.execute(query, (name, type, manufacturer, model, serial_number, purchase_date, warranty_expiration, location, status, pin_number, range_min, range_max, measure_unit, last_used, value))
        self.connection.commit()

    def update_device(self, device_id: int, **kwargs):
        updates = []
        params = []

        for key, value in kwargs.items():
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

    def get_all_devices(self) -> list[dict[str, str]]:
        query = "SELECT * FROM devices;"
        cursor = self.connection.execute(query)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def delete_device(self, device_id: int):
        self.connection.execute("DELETE FROM devices WHERE device_id = ?;", (device_id,))
        self.connection.commit()