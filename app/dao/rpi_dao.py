from app.services.db import DBManager

class GPIOControlDAO:
    def __init__(self):
        self.db_manager = DBManager()
        self.db_manager.reset_db_settings("sqlite-rpi")
        self.connection = DBManager().get_db_connection()

    def insert_or_ignore(self, pin_number: int, name: str, mode: str, state: str, pull: str):
        query = """
        INSERT OR IGNORE INTO gpio_pins (pin_number, name, mode, state, pull)
        VALUES (?, ?, ?, ?, ?);
        """
        self.connection.execute(query, (pin_number, name, mode, state, pull))
        self.connection.commit()

    def update_pin(self, pin_number: int, mode: str = None, state: str = None, pull: str = None):
        updates = []
        params = []

        if mode:
            updates.append("mode = ?")
            params.append(mode)
        if state:
            updates.append("state = ?")
            params.append(state)
        if pull:
            updates.append("pull = ?")
            params.append(pull)

        params.append(pin_number)
        query = f"""
        UPDATE gpio_pins
        SET {', '.join(updates)}
        WHERE pin_number = ?;
        """
        self.connection.execute(query, params)
        self.connection.commit()

    def get_all_pins(self) -> list[dict[str, str]]:
        query = "SELECT * FROM gpio_pins;"
        cursor = self.connection.execute(query)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def delete_all(self):
        self.connection.execute("DELETE FROM gpio_pins;")
        self.connection.commit()