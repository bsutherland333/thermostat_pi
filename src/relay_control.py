import RPi.GPIO as GPIO
from enum import Enum


class RelayType(Enum):
    FAN = 16
    HEAT = 18
    COOL = 22


class RelayControl:
    def __init__(self, relay: RelayType):
        self._relay_pin = relay.value
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._relay_pin, GPIO.OUT, initial=GPIO.HIGH)

        self.control_active = False

    def on(self):
        GPIO.output(self._relay_pin, GPIO.LOW)
        self.control_active = True

    def off(self):
        GPIO.output(self._relay_pin, GPIO.HIGH)
        self.control_active = False
