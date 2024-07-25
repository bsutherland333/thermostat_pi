import RPi.GPIO as GPIO
from enum import Enum


class Relay(Enum):
    FAN = 16
    HEAT = 18
    COOL = 22


class RelayControl:
    def __init__(self, relay: Relay):
        self.relay = relay
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.relay, GPIO.OUT, initial=GPIO.LOW)

    def on(self):
        GPIO.output(self.relay, GPIO.HIGH)

    def off(self):
        GPIO.output(self.relay, GPIO.LOW)
