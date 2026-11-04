"""leds.py - three status lights on the breadboard.
  GREEN blinking  = everything is normal
  YELLOW solid    = warning (problem, but not critical)
  RED solid       = critical
Wiring for each LED: GPIO pin -> 220 ohm resistor -> LED long leg; LED short leg -> GND rail.
Set a pin to None if you do not use that LED."""
import time
from sim import SIMULATE

RED_PIN = 27
YELLOW_PIN = 5
GREEN_PIN = 22
_leds = None
_last = None
_green_state = False
_last_blink = 0

def _init():
    global _leds
    if _leds is None:
        from gpiozero import LED
        make = lambda pin: LED(pin) if pin is not None else None
        _leds = {"red": make(RED_PIN), "yellow": make(YELLOW_PIN), "green": make(GREEN_PIN)}

def set_status(overall):
    """overall is NORMAL, WARNING or CRITICAL."""
    global _last, _green_state, _last_blink
    
    if SIMULATE:
        return

    # Only re-initialize the lights if the status actually changed
    if overall != _last:
        _last = overall
        _init()
        # Turn everything off first
        for led in _leds.values():
            if led is not None:
                led.off()
        _green_state = False
        
    # Handle the manual blinking for the GREEN LED
    if overall == "NORMAL" and _leds["green"] is not None:
        now = time.time()
        # Toggle the LED every 1 second
        if now - _last_blink >= 1.0:
            _last_blink = now
            _green_state = not _green_state
            if _green_state:
                _leds["green"].on()
            else:
                _leds["green"].off()
                
    elif overall == "WARNING" and _leds["yellow"] is not None:
        _leds["yellow"].on()
        
    elif overall == "CRITICAL" and _leds["red"] is not None:
        _leds["red"].on()

if __name__ == "__main__":                              # quick test: python3 leds.py
    print("Testing LED sequence. Watch the green LED blink.")
    for s in ("NORMAL", "WARNING", "CRITICAL", "NORMAL"):
        print(s)
        # Run the loop for 4 seconds to allow the green LED to blink
        for _ in range(8):
            set_status(s)
            time.sleep(0.5)