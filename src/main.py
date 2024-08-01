import time

from temp_sensor import TempSensor
from relay_control import RelayControl, RelayType
from logger import Logger


def main():
    sensor = TempSensor()
    fan = RelayControl(RelayType.FAN)
    cool = RelayControl(RelayType.COOL)
    heat = RelayControl(RelayType.HEAT)
    temp_log = Logger('/home/brandon/temp_log.csv', ['Temperature (C)', 'Temperature (F)'])
    status_log = Logger('/home/brandon/status_log.csv', ['Message'])

    status_log.log(['Starting temperature logging'])

    while True:
        temp = sensor.read_temp()
        print('Temperature:', temp)
        temp_log.log(temp)
        time.sleep(60)


if __name__ == '__main__':
    main()
