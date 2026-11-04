"""temperature.py - DHT11 Temperature Sensor using CircuitPython."""
import random
import time
from sim import SIMULATE, SIM

try:
    import board
    import adafruit_dht
    # DATA pin is on GPIO 4
    dht_device = adafruit_dht.DHT11(board.D4)
except Exception:
    dht_device = None

def read_temperature_c():
    if SIMULATE:
        if SIM["temp"] is not None:
            return SIM["temp"]
        return 22.0 + random.uniform(-0.3, 0.3)

    if dht_device is None:
        return None

    try:
        temperature = dht_device.temperature
        return temperature
    except Exception:
        return None

if __name__ == "__main__":
    print("Testing DHT11 Temperature Sensor...")
    for _ in range(10):
        t = read_temperature_c()
        if t is not None:
            print(f"Temperature: {t:.1f} C")
        else:
            print("Sensor not responding. Check wiring on GPIO 4.")
        time.sleep(2)