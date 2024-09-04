import time

from logger import Logger
from schedule import Schedule
from temp_control import TempControl, ControlMode
from temp_sensor import TempSensor


LOG_DIRECTORY = "/home/brandon/logs/"
SCHEDULE_FILEPATH = "/home/brandon/schedule.yaml"
# OVERRIDE_FILEPATH = "/home/brandon/override.yaml"


def main():
    # Initialize objects
    sensor = TempSensor()
    temp_log = Logger(
        "temperature", LOG_DIRECTORY, ["Temperature (C)", "Temperature (F)"]
    )
    status_log = Logger("status", LOG_DIRECTORY, ["Message"])
    schedule_log = Logger(
        "schedule",
        LOG_DIRECTORY,
        ["Minimum temperature (F)", "Maximum temperature (F)", "Mode"],
    )
    temp_control = TempControl(status_log)
    schedule = Schedule(SCHEDULE_FILEPATH)

    # Print starting messages
    print("Starting temperature control")
    status_log.log(["Starting temperature control"])

    # Main loop
    while True:
        # Get temperature
        temp = sensor.read_temp()
        print("Temperature (F):", temp[1])
        temp_log.log(temp)

        # Get the scheduled setpoints
        min, max, mode = schedule.get_setpoint()
        print("Schedule (F):", min, max, mode)
        schedule_log.log([min, max, mode])
        if mode == "heat":
            mode = ControlMode.HEAT
        elif mode == "cool":
            mode = ControlMode.COOL
        else:
            raise ValueError("Invalid mode")

        # Run control
        temp_control.run(min, max, temp[1], mode)

        # Wait for a while, since HVAC systems are slow
        time.sleep(30)


if __name__ == "__main__":
    main()
