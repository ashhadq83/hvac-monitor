"""vibration.py - blue vibration module (digital output DO on GPIO17). Owner: Member 2."""
import threading
import time

from sim import SIMULATE, SIM

_times = []
_lock = threading.Lock()
_sensor = None


def _on_pulse():
    with _lock:
        _times.append(time.time())


def _start():
    global _sensor
    if _sensor is None:
        from gpiozero import DigitalInputDevice
        _sensor = DigitalInputDevice(17, pull_up=None, active_state=True, bounce_time=0.01)
        _sensor.when_activated = _on_pulse


def vibration_events(window_s=3.0):
    """Number of vibration pulses detected in the last window_s seconds."""
    if SIMULATE:
        return int(SIM["vib"]) if SIM["vib"] is not None else 0
    _start()
    now = time.time()
    with _lock:
        while _times and now - _times[0] > window_s:
            _times.pop(0)
        return len(_times)


if __name__ == "__main__":                        # quick test: python3 vibration.py
    for _ in range(30):
        print(vibration_events())
        time.sleep(1)
