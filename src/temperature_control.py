import string
import yaml

from logger import Logger
from relay_control import RelayControl, RelayType
from temp_sensor import TempSensor


class TempControl:
    def __init__(self, temp_config_filepath: string, log_filepath):
        self._temp_config_filepath = temp_config_filepath

        self._heat_control = RelayControl(RelayType.HEAT)
        self._cool_control = RelayControl(RelayType.COOL)
        self._fan_control = RelayControl(RelayType.FAN)

        self._temp_sensor = TempSensor()

        self._temp_log = Logger("temperature", log_filepath, ["Temperature (C)", "Temperature (F)"])
        self._control_log = Logger("control", log_filepath, ["Control action"])
        self._control_log.log("Control initialized")

    def run_control():
        config = self._get_config()

    def _get_config():
        with open(self._temp_config_filepath, 'r') as file:
            return yaml.safe_load(file)
