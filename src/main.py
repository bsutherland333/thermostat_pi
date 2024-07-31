import time

from temp_sensor import TempSensor
from relay_control import RelayControl, RelayType


def main():
    sensor = TempSensor()
    fan = RelayControl(RelayType.FAN)
    cool = RelayControl(RelayType.COOL)
    heat = RelayControl(RelayType.HEAT)

    while True:
        temp_f = sensor.read_temp()[1]
        print(f'Current temp: {temp_f}')
        if temp_f < 69.0:
            cool.off()
        elif temp_f > 72.0:
            cool.on()
        time.sleep(10)

if __name__ == '__main__':
    main()
