import time

from logger import Logger
from relay_control import RelayType, RelayControl
from temp_sensor import TempSensor

LOG_PATH = "/home/brandon/logs/"

def main():
    heat = RelayControl(RelayType.HEAT)
    cool = RelayControl(RelayType.COOL)
    fan = RelayControl(RelayType.FAN)

    sensor = TempSensor()
    temp_log = Logger("temperature", LOG_PATH, ["Temperature (C)", "Temperature (F)"])
    status_log = Logger("status", LOG_PATH, ["Message"])

    print("Starting temperature logging")
    status_log.log(["Starting temperature logging"])

    while True:
        temp = sensor.read_temp()
        print("Temperature:", temp)
        temp_log.log(temp)
        time.sleep(60)


if __name__ == "__main__":
    main()
