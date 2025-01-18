import sqlite3

class GPIOControlDAO:
    def __init__(self):
        self.connection = None

    def set_database(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS gpio_pins (
            pin_number INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            mode TEXT CHECK(mode IN ('INPUT', 'OUTPUT')), 
            state TEXT CHECK(state IN ('HIGH', 'LOW')) DEFAULT NULL,
            pull TEXT CHECK(pull IN ('PULL_UP', 'PULL_DOWN', 'NONE')) DEFAULT 'NONE'
        );
        """
        self.connection.execute(query)
        self.connection.commit()

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