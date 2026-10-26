"""leds.py - three status lights on the breadboard.
  GREEN blinking  = everything is normal
  YELLOW solid    = warning (problem, but not critical)
  RED solid       = critical
Wiring for each LED: GPIO pin -> 220 ohm resistor -> LED long leg; LED short leg -> GND rail.
Set a pin to None if you do not use that LED."""
from sim import SIMULATE

RED_PIN = 27
YELLOW_PIN = 5
GREEN_PIN = 22
_leds = None
_last = None


def _init():
    global _leds
    if _leds is None:
        from gpiozero import LED
        make = lambda pin: LED(pin) if pin is not None else None
        _leds = {"red": make(RED_PIN), "yellow": make(YELLOW_PIN), "green": make(GREEN_PIN)}


def set_status(overall):
    """overall is NORMAL, WARNING or CRITICAL."""
    global _last
    if SIMULATE or overall == _last:
        return
    _last = overall
    _init()
    for led in _leds.values():
        if led is not None:
            led.off()                                   # also stops any blinking
    if overall == "CRITICAL" and _leds["red"] is not None:
        _leds["red"].on()
    elif overall == "WARNING" and _leds["yellow"] is not None:
        _leds["yellow"].on()
    elif overall == "NORMAL" and _leds["green"] is not None:
        _leds["green"].blink(on_time=1, off_time=1, background=True)


if __name__ == "__main__":                              # quick test: python3 leds.py
    import time
    for s in ("NORMAL", "WARNING", "CRITICAL", "NORMAL"):
        print(s)
        set_status(s)
        time.sleep(4)
