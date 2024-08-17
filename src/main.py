import time

from logger import Logger
from temp_sensor import TempSensor


LOG_DIRECTORY = "/home/brandon/logs/"


def main():
    sensor = TempSensor()
    temp_log = Logger("temperature", LOG_DIRECTORY, ["Temperature (C)", "Temperature (F)"])
    status_log = Logger("status", LOG_DIRECTORY, ["Message"])

    print("Starting temperature logging")
    status_log.log(["Starting temperature logging"])

    while True:
        temp = sensor.read_temp()
        print("Temperature:", temp)
        temp_log.log(temp)
        time.sleep(60)


if __name__ == "__main__":
    main()
