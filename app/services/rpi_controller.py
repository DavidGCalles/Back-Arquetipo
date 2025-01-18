from app.dao.rpi_dao import GPIOControlDAO
from app.services.rpi_cao import GPIOControlCAO

class GPIOController:
    def __init__(self, db_path: str):
        self.dao = GPIOControlDAO()
        self.dao.set_database(db_path)
        self.cao = GPIOControlCAO()

    def setup_pins_from_db(self):
        pins = self.dao.get_all_pins()

        for pin in pins:
            pin_number = pin["pin_number"]
            mode = pin["mode"]
            pull = pin["pull"] if pin["pull"] != "NONE" else None

            if mode:
                self.cao.setup_pin(pin_number, mode, pull)

    def setup_and_save_pin(self, pin_number: int, name: str, mode: str, pull: str = None):
        self.cao.setup_pin(pin_number, mode, pull)
        self.dao.insert_or_ignore(pin_number, name, mode, None, pull or "NONE")

    def write_and_update_pin(self, pin_number: int, state: str):
        self.cao.write_pin(pin_number, state)
        self.dao.update_pin(pin_number, state=state)

    def read_pin_and_sync(self, pin_number: int) -> str:
        state = self.cao.read_pin(pin_number)
        self.dao.update_pin(pin_number, state=state)
        return state

    def cleanup_all(self):
        self.cao.cleanup_all()
        #self.dao.delete_all()