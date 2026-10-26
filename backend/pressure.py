"""pressure.py - pressure change sensor. Owner: Member 3.
PRESSURE_SENSOR = "bmp180"      BMP180 module on I2C (address 0x77), in a sealed container
PRESSURE_SENSOR = "mpxv7002dp"  differential sensor read through ADS1115 channel A1
Both report pressure change in pascals relative to the start-up value."""
import random
import time

from sim import SIMULATE, SIM

PRESSURE_SENSOR = "bmp180"
OSS = 3                         # BMP180 oversampling (0-3); 3 = least noise
BMP_ADDR = 0x77
_bus = None
_cal = None
_baseline = None                # absolute pressure at start-up (BMP180) or zero volts (MPXV)


def _idiv(a, b):
    """Integer division that truncates toward zero, like the C code in the datasheet."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def bmp180_compute(ut, up, c, oss=OSS):
    """Datasheet algorithm. Returns (temperature in 0.1 C, pressure in Pa).
    Shifts (>>) round down and divisions (/) truncate, exactly like the C code in the datasheet."""
    x1 = ((ut - c["AC6"]) * c["AC5"]) >> 15
    x2 = _idiv(c["MC"] << 11, x1 + c["MD"])
    b5 = x1 + x2
    temp = (b5 + 8) >> 4
    b6 = b5 - 4000
    x1 = (c["B2"] * ((b6 * b6) >> 12)) >> 11
    x2 = (c["AC2"] * b6) >> 11
    x3 = x1 + x2
    b3 = _idiv(((c["AC1"] * 4 + x3) << oss) + 2, 4)
    x1 = (c["AC3"] * b6) >> 13
    x2 = (c["B1"] * ((b6 * b6) >> 12)) >> 16
    x3 = (x1 + x2 + 2) >> 2
    b4 = (c["AC4"] * (x3 + 32768)) >> 15
    b7 = (up - b3) * (50000 >> oss)
    p = _idiv(b7 * 2, b4) if b7 < 0x80000000 else _idiv(b7, b4) * 2
    x1 = (p >> 8) * (p >> 8)
    x1 = (x1 * 3038) >> 16
    x2 = (-7357 * p) >> 16
    p = p + ((x1 + x2 + 3791) >> 4)
    return temp, p


def _get_bus():
    global _bus
    if _bus is None:
        import smbus
        _bus = smbus.SMBus(1)
    return _bus


def _s16(msb, lsb):
    v = (msb << 8) | lsb
    return v - 65536 if v & 0x8000 else v


def _bmp_calibration():
    global _cal
    if _cal is None:
        d = _get_bus().read_i2c_block_data(BMP_ADDR, 0xAA, 22)
        w = lambda i: (d[i] << 8) | d[i + 1]
        s = lambda i: _s16(d[i], d[i + 1])
        _cal = {"AC1": s(0), "AC2": s(2), "AC3": s(4), "AC4": w(6), "AC5": w(8), "AC6": w(10),
                "B1": s(12), "B2": s(14), "MB": s(16), "MC": s(18), "MD": s(20)}
    return _cal


def bmp180_pressure_pa():
    """Absolute air pressure in pascals from the BMP180."""
    bus, cal = _get_bus(), _bmp_calibration()
    bus.write_byte_data(BMP_ADDR, 0xF4, 0x2E)
    time.sleep(0.006)
    d = bus.read_i2c_block_data(BMP_ADDR, 0xF6, 2)
    ut = (d[0] << 8) | d[1]
    bus.write_byte_data(BMP_ADDR, 0xF4, 0x34 + (OSS << 6))
    time.sleep(0.030)
    d = bus.read_i2c_block_data(BMP_ADDR, 0xF6, 3)
    up = ((d[0] << 16) | (d[1] << 8) | d[2]) >> (8 - OSS)
    return bmp180_compute(ut, up, cal)[1]


def _mpxv_sensor_volts():
    import ads1115
    return ads1115.read_volts(1) * 1.5          # undo the 10k / 20k divider (x 3/2)


def _raw():
    return bmp180_pressure_pa() if PRESSURE_SENSOR == "bmp180" else _mpxv_sensor_volts()


def calibrate_pressure_zero():
    """Call once at start-up while the sensor is at rest."""
    global _baseline
    if SIMULATE:
        return
    vals = []
    for _ in range(10):
        vals.append(_raw())
        time.sleep(0.05)
    _baseline = sum(vals) / len(vals)


def read_pressure_pa():
    """Pressure change in pascals (positive = pressure rise)."""
    global _baseline
    if SIMULATE:
        if SIM["pressure"] is not None:
            return SIM["pressure"]
        return random.uniform(-5, 5)
    if _baseline is None:
        calibrate_pressure_zero()
    value = _raw()
    if PRESSURE_SENSOR == "bmp180":
        delta = value - _baseline
        if abs(delta) < 40:                     # at rest: follow slow weather drift
            _baseline += 0.02 * delta
        return delta
    return (value - _baseline) * 1000.0          # MPXV7002DP: 1 V per kPa


if __name__ == "__main__":                        # quick test: python3 pressure.py
    calibrate_pressure_zero()
    print("Start-up value:", _baseline)
    for _ in range(40):
        print("%.0f Pa" % read_pressure_pa())
        time.sleep(0.5)
