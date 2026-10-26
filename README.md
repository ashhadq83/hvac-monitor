# HVAC Health Monitor (Raspberry Pi 4 B)

Sensors check the health of an HVAC system. Green blinking light = normal, yellow = warning,
red = critical. The screen and the phone app show the problem, what to do and who to contact
(explained by AI when an API key is set, otherwise by built-in rules).

```
hvac-monitor/
  backend/     Python: sensors, lights, AI advice, API on port 5000 + small web dashboard
  mobile/      Expo React TypeScript pages (Dashboard, Contacts, Settings)
  docs/        wiring picture and table
  setup.sh  run_backend.sh  run_mobile.sh  install_service.sh
```

## Step 1. Put this project on the Raspberry Pi
Open Raspberry Pi Connect, then click the black terminal icon. Pick ONE way:

* **Browser on the Pi:** email or upload `hvac-monitor-project.zip` to Google Drive on your laptop,
  then open the browser on the Pi, sign in and download it (it goes to `~/Downloads`).
* **From your laptop (PowerShell):** `scp hvac-monitor-project.zip YOUR-USER@YOUR-PI-NAME.local:~/`
  (run `whoami` and `hostname` in the Pi terminal to get the two names).
* **USB stick:** copy the zip to a stick and plug it into the Pi.

## Step 2. Unzip it
```bash
cd ~
sudo apt install -y unzip
unzip -o ~/Downloads/hvac-monitor-project.zip -d ~/
cd ~/hvac-monitor
```
(If the zip is not in Downloads, change the path.)

## Step 3. Run the one-time setup (about 10 to 20 minutes)
```bash
bash setup.sh
sudo reboot
```
It turns on I2C, installs Python packages and Node.js, builds the Expo app and copies our
pages into it. Reconnect after the reboot and `cd ~/hvac-monitor` again.

## Step 4. Wire the breadboard
Shut the Pi down and unplug it first. Follow `docs/breadboard_wiring.png` and `docs/WIRING.md`.

## Step 5. Check the sensors are seen
```bash
i2cdetect -y 1
```
You should see 48 (ADS1115) and 77 (BMP180). Test each part on its own:
```bash
cd ~/hvac-monitor/backend
python3 leds.py           # green blinks, then yellow, then red
python3 temperature.py    # about 20 to 25 C, rises when you hold the bead
python3 vibration.py      # jumps when you tap the table
python3 pressure.py       # near 0 Pa, changes when you squeeze the sealed container
```

## Step 6. Start the backend
```bash
cd ~/hvac-monitor
bash run_backend.sh
```
Open `http://localhost:5000` in the Pi browser. No hardware yet? Use fake data:
`HVAC_SIMULATE=1 bash run_backend.sh` and visit `/sim/pressure/900`, `/sim/temp/45`, `/sim/vib/12`.
Reset with `/sim/pressure/off`, `/sim/temp/off`, `/sim/vib/off`.

Leave this window running.

## Step 7. Start the mobile app (second terminal on the Pi)
```bash
cd ~/hvac-monitor
bash run_mobile.sh
```
A QR code appears. Install **Expo Go** on your phone, join the **same Wi-Fi as the Pi** and scan the
QR code (iPhone: Camera app, Android: inside Expo Go). The first load takes a minute or two.
The app finds the Pi's address by itself. If it cannot connect, open the Settings page and type
`http://PI-IP:5000` (run `hostname -I` on the Pi). If that fails too, try
`cd app && npx expo start --tunnel`, then use the Settings page.

## Step 8. AI advice (optional)
Create an API key at console.anthropic.com, then:
```bash
nano backend/.env        # paste the key after ANTHROPIC_API_KEY=
```
Save with Ctrl+X, Y, Enter, then restart the backend. Never share or upload `.env`.
Replace the DEMO contacts in `backend/technicians.json` with real local companies.

## Step 9. Start the backend automatically (optional)
```bash
bash install_service.sh
```

## Problems
* `i2cdetect` shows no 48 or 77: recheck the wires of that part and that I2C is on (Step 3, then reboot).
* Pressure barely moves: the BMP180 needs an airtight container fed by the syringe.
* Phone cannot connect: same Wi-Fi? Test `http://PI-IP:5000/api/status` in the phone browser.
* `python3 app.py` says port in use: another copy is running (`sudo systemctl stop hvac-backend`).
* Low-voltage warning on the Pi: use the official power supply directly in a wall outlet.
