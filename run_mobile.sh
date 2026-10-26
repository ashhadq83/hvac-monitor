#!/usr/bin/env bash
# Starts the Expo dev server on the Pi. Scan the QR code with Expo Go on your phone.
cd "$(dirname "$0")/app"
export REACT_NATIVE_PACKAGER_HOSTNAME="$(hostname -I | awk '{print $1}')"
exec npx expo start --lan
