import time

from temp_sensor import TempSensor
from relay_control import RelayControl, RelayType


def main():
    sensor = TempSensor()
    fan = RelayControl(RelayType.FAN)
    heat = RelayControl(RelayType.HEAT)
    cool = RelayControl(RelayType.COOL)

    while True:
        print(f"Temperature: {sensor.read_temp()[1]}°F")
        time.sleep(1)
