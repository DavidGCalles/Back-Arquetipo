from app.dao.rpi_dao import GPIOControlDAO
from app.services.rpi_cao import GPIOControlCAO

class GPIOController:
    def __init__(self):
        self.dao = GPIOControlDAO()
        self.cao = GPIOControlCAO()

    def _setup_pins_from_db(self):
        pins = self.dao.get_all_pins()
        for pin in pins:
            pin_number = pin["pin_number"]
            mode = pin["mode"]
            pull = pin["pull"] if pin["pull"] != "NONE" else None

            if mode:
                self.cao.setup_pin(pin_number, mode, pull)

    def setup_and_save_pin(self, pin_data: dict):
        """
        Setup a pin and save it to the database.
        keys in pin_data: pin_number, mode, pull
        
        Args:
            pin_data (dict): Pin data.
        """
        pin_number = pin_data["pin_number"]
        mode = pin_data["mode"]
        pull = pin_data["pull"] if pin_data["pull"] != "NONE" else None
        if self.cao.setup_pin(pin_number, mode, pull) and self.dao.insert_or_ignore(pin_data):
            return True
        return False

    def write_and_update_pin(self, pin_number: int, state: str):
        """
        Write to a pin and update the database.
        
        Args:
            pin_number (int): Pin number.
            state (str): Pin state.
        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        if self.cao.write_pin(pin_number, state) and self.dao.update_pin(pin_number, {"state": state}):
            return True
        return False

    def read_pin_and_sync(self, pin_number: int):
        """
        Read a pin and sync the database.
        
        Args:
            
            pin_number (int): Pin number.
        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        state = self.cao.read_pin(pin_number)
        if state:
            self.dao.update_pin(pin_number, {"state": state})
            return True
        return False

    def cleanup_all(self):
        self.cao.cleanup_all()