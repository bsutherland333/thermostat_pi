import time

from logger import Logger
from temp_sensor import TempSensor
from temp_control import TempControl, ControlMode


LOG_DIRECTORY = "/home/brandon/logs/"
#SCHEDULE_FILEPATH = "/home/brandon/schedule.yaml"
#OVERRIDE_FILEPATH = "/home/brandon/override.yaml"


def main():
    sensor = TempSensor()
    temp_log = Logger("temperature", LOG_DIRECTORY, ["Temperature (C)", "Temperature (F)"])
    status_log = Logger("status", LOG_DIRECTORY, ["Message"])
    temp_control = TempControl(status_log)

    print("Starting temperature control")
    status_log.log(["Starting temperature control"])

    while True:
        temp = sensor.read_temp()
        print("Temperature (F):", temp[1])
        temp_log.log(temp)

        temp_control.run(74, 75, temp[1], ControlMode.COOL)

        time.sleep(30)


if __name__ == "__main__":
    main()

