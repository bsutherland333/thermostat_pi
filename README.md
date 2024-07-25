# Thermostat Pi

This is basic code to turn a Raspberry Pi into a smart thermostat.
It uses a MCP9808 temperature sensor and a series of relays to control the heating, cooling, and fan.
I set this up on a Raspberry Pi Zero 2 W running Raspberry Pi OS Lite based on Debian Bookworm.

USE AT YOUR OWN RISK.
Modifying your HVAC system can result in freezing pipes and other damage. 
If you use this, wire up the pi such that your regular thermostat can still control the system to avoid freezing pipes.

I'm using this repository mostly as a place to back up and document my work, so expect some gaps.

## Parts List

- [Raspberry Pi Zero 2 W](https://www.raspberrypi.org/products/raspberry-pi-zero-2-w/)
- [MCP9808 temperature sensor](https://www.adafruit.com/product/1782)
- [4 5V Relay Module](https://www.amazon.com/SunFounder-Channel-Shield-Arduino-Raspberry/dp/B00E0NSORY/?th=1)
- [28VAC to 5VDC 2A converter](https://www.amazon.com/dp/B0BTSR2287?ref=ppx_yo2ov_dt_b_product_details&th=1)
- Reasonably Large Capacitor (not sure if necessary, but I had one lying around and it seemed like a good idea)
- Switch
- Various wires

## Wiring

### HVAC Wires

- Blue: Common wire, essentially a neutral wire that doesn't activate anything
- Red: 28VAC power wire
- Green: Fan wire, activates the fan when used as a neutral wire
- Yellow: Cooling wire, activates the cooling when used as a neutral wire
- White: Heating wire, activates the heating when used as a neutral wire

## Pi Software Setup

1. Enable I2C in `raspi-config` and install python3-smbus. 
Use i2cdetect to make sure the MCP9808 is working properly. 
You should see a device at address 0x18 in the grid output.
