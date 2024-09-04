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
- [28VAC to 5VDC 2A converter](https://www.amazon.com/UMLIFE-Converter-2-5-35V-Regulator-Adjustable/dp/B094ZTG5S8/?th=1)
- Switch
- Various wires

### Wiring

HVAC Wires

- Blue: Common wire, essentially a neutral wire that doesn't activate anything
- Red: 28VAC power wire
- Green: Fan wire, activates the fan when used as a neutral wire
- Yellow: Cooling wire, activates the cooling when used as a neutral wire
- White: Heating wire, activates the heating when used as a neutral wire

Pi Wiring

1. Wire the AC DC converter to the pi's 5v power and ground. I used pins 2 and 6.
2. Wire the temperature sensor to the pi's 3v power and ground, and then wire the sensor's I2C pins to the pi's SDA and SCL I2C pins. Specifically, these are pins 1, 3, 5, and 9.
3. Wire the relay board to the pi's 5v power and ground, and three of the pi's GPIO pins to the control pins on the relay board. Specifically, I used pins 4, 16, 18, 20, and 22.

Power Supply

1. Connect the AC input of the power supply to the red and blue HVAC wires.
2. Split the red wire leading to the power supply with a switch, and mount the switch in an easily accessible location on the thermostat.

Relay Board

1. Wire the relay to the pi as described in the pi wiring section.
2. Connect the green, yellow, and white wires to the nominally open terminal block three of the relays.
   Nominally open means that the connection with be open without input from the pi.
   Which terminal block is which is denoted by a symbol on the board.
3. Connect the red HVAC wire to the middle of the terminal connectors for each of the relays.
   I did this by connecting the first relay to the red wire, and then chained the next relay by connecting the nominally closed terminal on the current relay with the center terminal on the next relay.
   This means that only one system could ever be active at once, as enabling one would shut off the power to all systems after it.

### Pi Software Setup

1. Enable I2C in `raspi-config` and install python3-smbus.
Use i2cdetect to make sure the MCP9808 is working properly.
You should see a device at address 0x18 in the grid output.
2. Install all other packages in requirements.txt.
3. Create systemctl service to run script at startup.
   Here is an example of what the service file should look like, stored in `/etc/systemd/system/thermostat.service`:
   ```
   [Unit]
   Description=Run thermostat_pi
   After=network.target
   
   [Service]
   ExecStart=/usr/bin/python3 /home/brandon/thermostat_pi/src/main.py
   WorkingDirectory=/home/brandon/thermostat_pi
   Restart=always
   RestartSec=10
   User=brandon
   Environment=PYTHONUNBUFFERED=1
   
   [Install]
   WantedBy=multi-user.target
   ```
   Make sure to enable and start the service after rebooting the pi.

## Controlling the thermostat

The thermostat is controlled with a .yaml configuration file, with the filepath being set by a global variable in the main function.
The file consists of time entries in a 3-4 digit 24 hour format, with the first digits representing the hour of the day and the last two representing the minute of the hour.
Do not include leading zeros, as this will be interpreted as an octal number instead of a decimal number.

Each time entry has three parameters:
- `setpoint`:
  The temperature that the thermostat should control to, in units of fahrenheit.
  Usually one of the only things you have to worry about with a typical thermostat.
- `tolerance`:
  The range around which the temperature is allowed to move, in unit of fahrenheit.
  Thermostats use bang-bang control, which results in the temperature constantly going up and down around the setpoint as the heat/cool is switching between active and inactive.
  The tolerance is the distance away from the setpoint that the temperature is allowed to move within, making a zip-zag like pattern.
  The smaller this value is set to, the shorter but more frequent that the HVAC system will be on.
  Our analog thermostat has a tolerance of about 1 degree, which means that when set to 75 degrees, the temperature ranges from 74-76 degrees.
- `transition_period` (optional, default is 0):
  This specifies the rate in minutes at which the setpoint should transition from the previous setpoint to the new one.
  If set to zero, the setpoint will immediately jump from the previous value to the new value at the time for that entry.
  If set to something like 30 minutes, the setpoint will linearly transition from the previous value to the new value starting at the time of that entry.
- mode: (optional, default is auto)
  This specifies what mode to use for temperature control. There are three modes: heat, cool, and auto. Heat and cool specifies to only use heating or cooling respectively, while auto will use one or the other based on whether the ambient temperature is increasing or decreasing in time.

Config example:
```
500:
  setpoint: 75.0
  tolerance: 0.5
  transition_period: 30
  mode: auto

2200:
  setpoint: 70.0
  tolerance: 0.5
  transition_period: 120
  mode: auto
```
