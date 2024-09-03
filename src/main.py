import time

from logger import Logger
from temp_sensor import TempSensor
from temp_control import TempControl, ControlMode
from schedule import Schedule


LOG_DIRECTORY = "/home/brandon/logs/"
SCHEDULE_FILEPATH = "/home/brandon/schedule.yaml"
# OVERRIDE_FILEPATH = "/home/brandon/override.yaml"


def main():
    sensor = TempSensor()
    temp_log = Logger(
        "temperature", LOG_DIRECTORY, ["Temperature (C)", "Temperature (F)"]
    )
    status_log = Logger("status", LOG_DIRECTORY, ["Message"])
    temp_control = TempControl(status_log)
    schedule = Schedule(SCHEDULE_FILEPATH)

    print("Starting temperature control")
    status_log.log(["Starting temperature control"])

    while True:
        temp = sensor.read_temp()
        print("Temperature (F):", temp[1])
        temp_log.log(temp)

        min, max, mode = schedule.get_setpoint()
        if mode == "heat":
            mode = ControlMode.HEAT
        elif mode == "cool":
            mode = ControlMode.COOL
        else:
            raise RuntimeError("Auto mode not yet implemented")

        temp_control.run(min, max, temp[1], mode)

        time.sleep(30)


if __name__ == "__main__":
    main()
