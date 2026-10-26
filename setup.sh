#!/usr/bin/env bash
# One-time setup for the Raspberry Pi. Run from this folder:  bash setup.sh
set -e
cd "$(dirname "$0")"

echo "== 1/4  Turning on I2C =="
sudo raspi-config nonint do_i2c 0

echo "== 2/4  Installing Python packages =="
sudo apt update
sudo apt install -y python3-flask python3-smbus python3-gpiozero i2c-tools curl

echo "== 3/4  Installing Node.js (needed for the mobile app) =="
NODE_MAJOR=0
if command -v node >/dev/null 2>&1; then
  NODE_MAJOR=$(node -v | cut -d. -f1 | tr -d v)
fi
if [ "$NODE_MAJOR" -lt 20 ]; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo apt install -y nodejs
fi
node -v

echo "== 4/4  Creating the Expo app and copying our pages into it =="
if [ ! -d app ]; then
  npx --yes create-expo-app@latest app --template blank-typescript --no-install
fi
cp mobile/App.tsx app/App.tsx
rm -rf app/src
cp -r mobile/src app/src
(cd app && npm install && npx expo install expo-constants)

if [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
fi

echo
echo "Setup finished."
echo "Reboot once so I2C is active:  sudo reboot"
echo "Then see README.md, step 5 onwards."
