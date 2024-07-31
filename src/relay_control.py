import RPi.GPIO as GPIO
from enum import Enum


class RelayType(Enum):
    FAN = 16
    HEAT = 18
    COOL = 22


class RelayControl:
    def __init__(self, relay: RelayType):
        self.relay_pin = relay.value
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.relay_pin, GPIO.OUT, initial=GPIO.HIGH)

    def on(self):
        GPIO.output(self.relay_pin, GPIO.LOW)

    def off(self):
        GPIO.output(self.relay_pin, GPIO.HIGH)
