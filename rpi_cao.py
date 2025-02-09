import RPi.GPIO as GPIO

class GPIOControlCAO:
    """
    GPIOControlCAO: Class to manage the control of the GPIO pins.
    """
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # Usamos numeración BCM

    def setup_pin(self, pin_number: int, mode: str, pull: str = None, state: str = None):
        """
        Configura un pin GPIO.
        
        Args:
            pin_number (int): Número del pin.
            mode (str): Modo del pin (INPUT o OUTPUT).
            pull (str): Resistencia pull-up o pull-down (PULL_UP, PULL_DOWN o None).
            state (str): Estado inicial del pin (HIGH o LOW)."""
        if mode not in ("INPUT", "OUTPUT"):
            return False
        try:
            gpio_mode = GPIO.IN if mode == "INPUT" else GPIO.OUT

            pull_mode = None
            if pull == "PULL_UP":
                pull_mode = GPIO.PUD_UP
            elif pull == "PULL_DOWN":
                pull_mode = GPIO.PUD_DOWN

            if pull_mode:
                GPIO.setup(pin_number, gpio_mode, pull_up_down=pull_mode)
            else:
                GPIO.setup(pin_number, gpio_mode)

            if state:
                self.write_pin(pin_number, state)

            return True
        except Exception as e:
            return False

    def write_pin(self, pin_number: int, state: str):
        """
        Escribe un estado en un pin GPIO.

        Args:
            pin_number (int): Número del pin.
            state (str): Estado del pin (HIGH o LOW).
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        if state not in ("HIGH", "LOW"):
            return False
        try:
            gpio_state = GPIO.HIGH if state == "HIGH" else GPIO.LOW
            GPIO.output(pin_number, gpio_state)
            return True
        except Exception as e:
            return False

    def read_pin(self, pin_number: int):
        """
        Lee el estado de un pin GPIO.
        
        Args:
            pin_number (int): Número del pin.
        Returns:
            str: Estado del pin (HIGH o LOW).
        """ 
        try:
            state = GPIO.input(pin_number)
            return "HIGH" if state == GPIO.HIGH else "LOW"
        except Exception as e:
            return None

    def cleanup_all(self):
        GPIO.cleanup()

GPIOCAO = GPIOControlCAO()