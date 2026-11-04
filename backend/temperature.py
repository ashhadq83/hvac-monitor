"""temperature.py - DHT11 Temperature Sensor."""
import random
import time
from sim import SIMULATE, SIM

# Import the DHT11 library
try:
    import Adafruit_DHT
    SENSOR_TYPE = Adafruit_DHT.DHT11
    SENSOR_PIN = 4  # Make sure the DATA pin is wired to GPIO 4
except ImportError:
    SENSOR_TYPE = None

def read_temperature_c():
    """Return temperature in deg C, or None if the sensor is not responding."""
    if SIMULATE:
        if SIM["temp"] is not None:
            return SIM["temp"]
        return 22.0 + random.uniform(-0.3, 0.3)
    
    if SENSOR_TYPE is None:
        return None # Library missing

    try:
        # Read the sensor
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE, SENSOR_PIN)
        if temperature is not None:
            return temperature
        return None
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