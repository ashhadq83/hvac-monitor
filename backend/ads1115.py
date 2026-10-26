"""ads1115.py - minimal driver for the ADS1115 16-bit I2C converter (address 0x48).
Wiring: VDD to 3V3, GND to GND, SCL to SCL1, SDA to SDA1, ADDR to GND."""
import time

ADDR = 0x48
FULL_SCALE_V = 4.096          # programmable gain setting used below (+/- 4.096 V)
_bus = None


def _get_bus():
    global _bus
    if _bus is None:
        import smbus
        _bus = smbus.SMBus(1)
    return _bus


def read_volts(channel, bus=None):
    """Single-shot reading of input A<channel> measured against GND, in volts."""
    bus = bus or _get_bus()
    config = 0x8000 | (0x4000 + (channel << 12)) | 0x0200 | 0x0100 | 0x0080 | 0x0003
    bus.write_i2c_block_data(ADDR, 0x01, [config >> 8, config & 0xFF])
    for _ in range(50):                       # wait until the conversion is finished
        time.sleep(0.002)
        hi, lo = bus.read_i2c_block_data(ADDR, 0x01, 2)
        if hi & 0x80:
            break
    hi, lo = bus.read_i2c_block_data(ADDR, 0x00, 2)
    raw = (hi << 8) | lo
    if raw & 0x8000:
        raw -= 65536
    return raw * FULL_SCALE_V / 32768.0
