# Breadboard wiring (see breadboard_wiring.png)

Hold the board with the red T-cobbler at the TOP. Rows = printed numbers (1 at the bottom).
Left half = columns a-e, right half = f-j. Left rail pair: red line = 3V3 (+), blue line = GND (-).
Cobbler wires go into a free hole in the SAME ROW as the cobbler label, on the left side.
Power the Pi off before changing any wire. Never use 5V for anything in this circuit.

| ID | From | To |
|---|---|---|
| W1 | cobbler 3V3 | red rail, row 25 |
| W2 | cobbler GND | blue rail, row 24 |
| ADS1115 | pins in column e, rows 30 down to 21 (VDD at row 30, then GND, SCL, SDA, ADDR, ALRT, A0, A1, A2, A3) | |
| W3 | a30 (VDD) | red rail |
| W4 | a29 (GND) | blue rail |
| W5 | d28 (SCL) | cobbler SCL1 |
| W6 | c27 (SDA) | cobbler SDA1 |
| W7 | a26 (ADDR) | blue rail |
| W8 | d24 (A0) | d16 |
| R1 | 100 kOhm resistor | b17 to b16 |
| W9 | a17 | red rail |
| T1, T2 | thermistor wires | c16 and c15 |
| W10 | a15 | blue rail |
| B1, B2 | BMP180 VCC, GND | red rail row 22, blue rail row 21 |
| B3, B4 | BMP180 SCL, SDA | b28, b27 |
| V1, V2 | vibration VCC, GND | red rail row 19, blue rail row 18 |
| V3 | vibration DO | cobbler GPIO17 |
| W12 | cobbler GPIO27 | a12; 220 ohm b12-b11; RED LED long leg c11, short leg c10; W13 a10 to blue rail |
| W14 | cobbler GPIO5 | a8; 220 ohm b8-b7; YELLOW LED long c7, short c6; W15 a6 to blue rail |
| W16 | cobbler GPIO22 | a4; 220 ohm b4-b3; GREEN LED long c3, short c2; W17 a2 to blue rail |

Lights: GREEN blinking = normal, YELLOW = warning, RED = critical.
