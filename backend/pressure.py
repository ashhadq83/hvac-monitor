"""pressure.py - Ultrasonic Distance Sensor simulating Airflow Blockage."""
import random
import time
from sim import SIMULATE, SIM

# Import gpiozero for the HC-SR04
# Make sure Trig is wired to GPIO 23 and Echo to GPIO 24
try:
    from gpiozero import DistanceSensor
    sensor = DistanceSensor(echo=24, trigger=23, max_distance=2.0)
except Exception:
    sensor = None

def calibrate_pressure_zero():
    # The app expects this function to exist at startup, but we don't need it for ultrasonic
    pass

def read_pressure_pa():
    """Returns a simulated pressure (Pa) based on the distance to an object."""
    if SIMULATE:
        if SIM["pressure"] is not None:
            return SIM["pressure"]
        return random.uniform(-5, 5)
    
    if sensor is None:
        return None

    try:
        # Get distance in cm
        distance_cm = sensor.distance * 100
        
        # Map distance to a fake pressure value to trigger alerts in the app
        if distance_cm < 10:
            return 800.0  # Triggers CRITICAL (someone is blocking the vent)
        elif distance_cm < 20:
            return 300.0  # Triggers WARNING (partial blockage)
        else:
            return 0.0    # NORMAL (clear airflow)
    except Exception:
        return None

if __name__ == "__main__":
    print("Testing HC-SR04 Ultrasonic Sensor...")
    print("Wave your hand in front of the sensor to see the values change.")
    for _ in range(40):
        if sensor:
            dist = sensor.distance * 100
            p = read_pressure_pa()
            print(f"Distance: {dist:.1f} cm | Simulated Pressure: {p} Pa")
        else:
            print("Sensor not initialized. Check wiring.")
        time.sleep(1)