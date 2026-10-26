"""sim.py - simulation switch shared by all modules.
Set the environment variable HVAC_SIMULATE=1 to run without any hardware."""
import os

SIMULATE = os.environ.get("HVAC_SIMULATE") == "1"

# Manual overrides used only in simulation mode (set through the /sim/ web routes)
SIM = {"temp": None, "pressure": None, "vib": None}
