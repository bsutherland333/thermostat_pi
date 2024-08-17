# Thermostat Pi

This is basic code to turn a Raspberry Pi into a smart thermostat.
It uses a MCP9808 temperature sensor and a series of relays to control the heating, cooling, and fan.
I set this up on a Raspberry Pi Zero 2 W running Raspberry Pi OS Lite based on Debian Bookworm.

USE AT YOUR OWN RISK.
Modifying your HVAC system can result in freezing pipes and other damage. 
If you use this, wire up the pi such that your regular thermostat can still control the system to avoid freezing pipes.

I'm using this repository mostly as a place to back up and document my work, so expect some gaps.

## Setup

### Parts List

- [Raspberry Pi Zero 2 W](https://www.raspberrypi.org/products/raspberry-pi-zero-2-w/)
- [MCP9808 temperature sensor](https://www.adafruit.com/product/1782)
- [4 5V Relay Module](https://www.amazon.com/SunFounder-Channel-Shield-Arduino-Raspberry/dp/B00E0NSORY/?th=1)
- [28VAC to 5VDC 2A converter](https://www.amazon.com/dp/B0BTSR2287?ref=ppx_yo2ov_dt_b_product_details&th=1)
- Reasonably Large Capacitor (not sure if necessary, but I had one lying around and it seemed like a good idea)
- Switch
- Various wires

### Wiring

HVAC Wires

- Blue: Common wire, essentially a neutral wire that doesn't activate anything
- Red: 28VAC power wire
- Green: Fan wire, activates the fan when used as a neutral wire
- Yellow: Cooling wire, activates the cooling when used as a neutral wire
- White: Heating wire, activates the heating when used as a neutral wire

Pi Software Setup

1. Enable I2C in `raspi-config` and install python3-smbus. 
Use i2cdetect to make sure the MCP9808 is working properly. 
You should see a device at address 0x18 in the grid output.

## Controlling the thermostat

The thermostat is controlled with a .yaml configuration file, with the filepath being set by a global variable in the main function.
The file consists of time entries in a 4 digit 24 hour format, with the first two digits representing the hour of the day and the last two representing the minute of the hour.

Each time entry has three parameters:
- `setpoint`
  The temperature that the thermostat should control to, in units of fahrenheit.
  Usually one of the only things you have to worry about with a typical thermostat.
- `tolerance`
  The range around which the temperature is allowed to move, in unit of fahrenheit.
  Thermostats use bang-bang control, which results in the temperature constantly going up and down around the setpoint as the heat/cool is switching between active and inactive.
  The tolerance is the distance away from the setpoint that the temperature is allowed to move within, making a zip-zag like pattern.
  The smaller this value is set to, the shorter but more frequent that the HVAC system will be on.
  Our analog thermostat has a tolerance of about 1 degree, which means that when set to 75 degrees, the temperature ranges from 74-76 degrees.
- `transition_period` (optional, default is 0)
  This specifies the rate in minutes at which the setpoint should transition from the previous setpoint to the new one.
  If set to zero, the setpoint will immediately jump from the previous value to the new value at the time for that entry.
  If set to something like 30 minutes, the setpoint will linearly transition from the previous value to the new value starting at the time of that entry.

The mode to use for temperature control isn't specified here, as the thermostat will automatically detect whether the ambient temperature is increasing in time (therefore needing cooling) or decreasing in time (therefore needing heating).
To minimize energy usage, the thermostat will wait for the ambient temperature to increase or decrease to the setpoint and will not actively push it there.

Config example:
```
0500:
  setpoint: 75.0
  tolerance: 0.5
  transition_period: 30

2200:
  setpoint: 70.0
  tolerance: 0.5
  transition_period: 120
```
