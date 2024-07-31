import time

from temp_sensor import TempSensor
from relay_control import RelayControl, RelayType
from logger import log_data


def main():
    sensor = TempSensor()
    fan = RelayControl(RelayType.FAN)
    cool = RelayControl(RelayType.COOL)
    heat = RelayControl(RelayType.HEAT)

    while True:
        fan.off()
        cool.off()
        heat.off()
        temp_f = sensor.read_temp()[1]
        print('Temperature:', temp_f)
        log_data(temp_f, '/home/brandon/temperature_log.csv')
        time.sleep(30)

if __name__ == '__main__':
    main()
