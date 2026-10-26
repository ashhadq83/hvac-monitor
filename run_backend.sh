#!/usr/bin/env bash
# Starts the Python backend (sensors, lights, AI advice, API on port 5000).
#   bash run_backend.sh              uses the real sensors
#   HVAC_SIMULATE=1 bash run_backend.sh   no hardware needed (fake data)
cd "$(dirname "$0")/backend"
echo "Backend address on your network:  http://$(hostname -I | awk '{print $1}'):5000"
exec python3 app.py
