#!/usr/bin/env bash
# Optional: start the backend automatically every time the Pi powers on.
#   bash install_service.sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
sudo tee /etc/systemd/system/hvac-backend.service >/dev/null <<UNIT
[Unit]
Description=HVAC Health Monitor backend
After=network-online.target
Wants=network-online.target

[Service]
User=$USER
WorkingDirectory=$DIR/backend
ExecStart=/usr/bin/python3 $DIR/backend/app.py
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
UNIT
sudo systemctl daemon-reload
sudo systemctl enable --now hvac-backend
echo "Backend installed. Check it with:  sudo systemctl status hvac-backend"
