from enum import Enum

from logger import Logger
from relay_control import RelayControl, RelayType


class ControlMode(Enum):
    HEAT = 0
    COOL = 1


class TempControl:
    def __init__(self, status_log: Logger):
        self._status_log = status_log

        self._heat_control = RelayControl(RelayType.HEAT)
        self._cool_control = RelayControl(RelayType.COOL)

    def run_control(min_temp: float, max_temp: float, curr_temp: float, mode: ControlMode):
        if mode == ControlMode.HEAT:
            # Make sure cool is off
            if self._cool_control.control_active:
                self._cool_control.off()

            # Control is on and needs to shut off
            if curr_temp > max_temp and self._heat_control.control_active:
                self._heat_control.off()
                print('Heat off')
                self._status_log.log(['Heat off'])
                return

            # Control is off and needs to turn on
            if curr_temp < min_temp and not self._heat_control.control_active:
                self._heat_control.on()
                print('Heat on')
                self._status_log.log(['Heat on'])
                return

        else:  # ControlMode.COOL
            # Make sure heat is off
            if self._heat_control.control_active:
                self._heat_control.off()

            # Control is on and needs to shut off
            if curr_temp < min_temp and self._cool_control.control_active:
                self._cool_control.off()
                print('Cool off')
                self._status_log.log(['Cool off'])
                return

            # Control is off and needs to turn on
            if curr_temp > max_temp and not self._cool_control.control_active:
                self._cool_control.on()
                print('Cool on')
                self._status_log.log(['Cool on'])
                return

