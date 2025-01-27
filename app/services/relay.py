"""Class to control a relay with a GPIO pin."""
import RPi.GPIO as GPIO

class Relay:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def toogle(self, desired_state: bool = None):
        if desired_state is None:
            desired_state = not self.is_on()
        if desired_state:
            self.on()
        else:
            self.off()
    def is_on(self):
        return GPIO.input(self.pin) == GPIO.HIGH