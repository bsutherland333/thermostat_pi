import smbus


# Device addresses
_DEFAULT_ADDRESS = 0x18
_DEVICE_ID = 0x54

# Registers
_REG_CONFIGURATION = 0x01
_REG_UPPER_TEMP = 0x02
_REG_LOWER_TEMP = 0x03
_REG_CRITICAL_TEMP = 0x04
_REG__TEMP = 0x05
_REG_MANUFACTURER_ID = 0x06
_REG_DEVICE_ID = 0x07
_REG_RESOLUTION = 0x08

# Resolution values
_RESOLUTION_HALF_C = 0x0
_RESOLUTION_QUARTER_C = 0x1
_RESOLUTION_EIGHTH_C = 0x2
_RESOLUTION_SIXTEENTH_C = 0x3


class TempSensor:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(_DEFAULT_ADDRESS, _REG_CONFIGURATION, _RESOLUTION_SIXTEENTH_C)

    def read_temp(self) -> (float, float):
        """
        Read the temperature from the MCP9808 sensor
        :return: The temperature in Celsius and Fahrenheit
        """
        data = self.bus.read_i2c_block_data(_DEFAULT_ADDRESS, _REG__TEMP, 2)
        temp_c = ((data[0] << 8 | data[1]) & 0xFFF) / 16
        temp_f = temp_c * 1.8 + 32
        return temp_c, temp_f
