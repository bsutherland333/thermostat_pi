import time

from temp_sensor import TempSensor
from logger import Logger

LOG_PATH = "/home/brandon/thermostat_logs/"

def main():
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
