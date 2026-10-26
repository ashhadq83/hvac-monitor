"""temperature.py - 100k NTC 3950 thermistor read through the ADS1115 (channel A0).
Circuit: 3V3 -> fixed resistor -> middle point -> thermistor -> GND.
The middle point goes to ADS1115 A0. Owner: Member 2."""
import math
import random
import time

from sim import SIMULATE, SIM

VCC = 3.3
R_FIXED = 100000.0      # ohms. Use 10000.0 here if you built the divider with a 10k resistor.
R0 = 100000.0           # thermistor resistance at 25 C
T0 = 298.15             # 25 C in kelvin
BETA = 3950.0
CHANNEL = 0
OFFSET_C = 0.0          # calibration: add or subtract degrees after comparing with a thermometer


def volts_to_celsius(v, vcc=VCC, r_fixed=R_FIXED):
    """Convert the divider middle-point voltage to degrees C (None if out of range)."""
    if v <= 0.01 or v >= vcc - 0.01:
        return None
    r = r_fixed * v / (vcc - v)                       # thermistor resistance
    inv_t = 1.0 / T0 + math.log(r / R0) / BETA        # beta equation
    return 1.0 / inv_t - 273.15


def read_temperature_c():
    """Return temperature in deg C, or None if the sensor is not responding."""
    if SIMULATE:
        if SIM["temp"] is not None:
            return SIM["temp"]
        return 22.0 + random.uniform(-0.3, 0.3)
    try:
        import ads1115
        v = sum(ads1115.read_volts(CHANNEL) for _ in range(4)) / 4
        t = volts_to_celsius(v)
        return None if t is None else t + OFFSET_C
    except Exception:
        return None


if __name__ == "__main__":                            # quick test: python3 temperature.py
    for _ in range(20):
        print(read_temperature_c())
        time.sleep(1)
