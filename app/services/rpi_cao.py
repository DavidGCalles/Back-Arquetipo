import RPi.GPIO as GPIO

class GPIOControlCAO:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # Usamos numeración BCM
        self.active_pins = set()  # Lleva un control de los pines configurados

    def setup_pin(self, pin_number: int, mode: str, pull: str = None):
        if mode not in ("INPUT", "OUTPUT"):
            raise ValueError("El modo debe ser 'INPUT' o 'OUTPUT'.")

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

        self.active_pins.add(pin_number)

    def write_pin(self, pin_number: int, state: str):
        if pin_number not in self.active_pins:
            raise RuntimeError(f"El pin {pin_number} no está configurado.")
        if state not in ("HIGH", "LOW"):
            raise ValueError("El estado debe ser 'HIGH' o 'LOW'.")

        gpio_state = GPIO.HIGH if state == "HIGH" else GPIO.LOW
        GPIO.output(pin_number, gpio_state)

    def read_pin(self, pin_number: int) -> str:
        if pin_number not in self.active_pins:
            raise RuntimeError(f"El pin {pin_number} no está configurado.")

        state = GPIO.input(pin_number)
        return "HIGH" if state == GPIO.HIGH else "LOW"

    def cleanup_pin(self, pin_number: int):
        if pin_number in self.active_pins:
            GPIO.cleanup(pin_number)
            self.active_pins.remove(pin_number)

    def cleanup_all(self):
        GPIO.cleanup()
        self.active_pins.clear()