"""app.py - dashboard server and alert logic for the HVAC Health Monitor.
Backend of the HVAC Health Monitor (API on port 5000 + small web dashboard).
  On the Pi:         python3 app.py
  Without hardware:  HVAC_SIMULATE=1 python3 app.py
"""
import threading
import time

from flask import Flask, jsonify, abort

import advisor
import leds
import pressure
import sim
import temperature
import vibration

advisor.load_env()
app = Flask(__name__)

# ---- Thresholds (tune these during testing) ----
TEMP_WARN_LOW, TEMP_CRIT_LOW = 16.0, 8.0       # deg C
TEMP_WARN_HIGH, TEMP_CRIT_HIGH = 28.0, 40.0    # deg C
PRESS_WARN, PRESS_CRIT = 250.0, 750.0          # Pa change (absolute value)
VIB_WARN, VIB_CRIT = 3, 10                     # pulses in the last 3 seconds

RANK = {"NORMAL": 0, "WARNING": 1, "CRITICAL": 2}

state = {
    "temp_c": None, "pressure_pa": None, "vib_events": 0,
    "temp_status": "NORMAL", "pressure_status": "NORMAL", "vib_status": "NORMAL",
    "overall": "NORMAL", "alerts": [], "advice": advisor.advice,
}


def classify_temp(t):
    if t is None:
        return "WARNING", "Temperature sensor not responding"
    if t >= TEMP_CRIT_HIGH or t <= TEMP_CRIT_LOW:
        return "CRITICAL", "Temperature critical: %.1f C - check system efficiency" % t
    if t >= TEMP_WARN_HIGH or t <= TEMP_WARN_LOW:
        return "WARNING", "Temperature out of range: %.1f C" % t
    return "NORMAL", ""


def classify_pressure(p):
    if p is None:
        return "WARNING", "Pressure sensor not responding"
    if abs(p) >= PRESS_CRIT:
        return "CRITICAL", "Severe pressure change (%+.0f Pa) - filter may be clogged" % p
    if abs(p) >= PRESS_WARN:
        return "WARNING", "Airflow restriction (%+.0f Pa) - inspect filter" % p
    return "NORMAL", ""


def classify_vibration(n):
    if n >= VIB_CRIT:
        return "CRITICAL", "Excess vibration - schedule maintenance"
    if n >= VIB_WARN:
        return "WARNING", "Vibration detected - check mechanical wear"
    return "NORMAL", ""


def sensor_loop():
    try:
        pressure.calibrate_pressure_zero()
    except Exception:
        pass
    while True:
        t = temperature.read_temperature_c()
        try:
            p = pressure.read_pressure_pa()
        except Exception:
            p = None
        v = vibration.vibration_events()
        ts, tmsg = classify_temp(t)
        ps, pmsg = classify_pressure(p)
        vs, vmsg = classify_vibration(v)
        overall = max((ts, ps, vs), key=lambda s: RANK[s])
        problems = [{"sensor": n, "status": s, "message": m, "value": val}
                    for n, s, m, val in (("pressure", ps, pmsg, p), ("temperature", ts, tmsg, t),
                                         ("vibration", vs, vmsg, v)) if s != "NORMAL"]
        try:
            leds.set_status(overall)
        except Exception:
            pass
        advisor.update(problems)
        state.update(
            temp_c=t, pressure_pa=p, vib_events=v,
            temp_status=ts, pressure_status=ps, vib_status=vs, overall=overall,
            alerts=[x["message"] for x in problems], advice=advisor.advice,
        )
        time.sleep(1)


PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HVAC Health Monitor</title>
<style>
body{font-family:Arial,sans-serif;background:#0b1a2e;color:#fff;margin:0;
     padding:20px;text-align:center}
h1{margin:0 0 4px}
.sub{color:#8fb3c9;margin-bottom:20px}
.cards{display:flex;flex-wrap:wrap;justify-content:center;gap:16px}
.card{width:220px;padding:18px;border-radius:14px;background:#14284a;
      border:3px solid #00cc77}
.card.WARNING{border-color:#ffb020;background:#2b2108}
.card.CRITICAL{border-color:#ff3b3b;background:#2e0b0b}
.label{font-size:13px;color:#9fb6c9;letter-spacing:1px}
.value{font-size:34px;font-weight:bold;margin:10px 0}
.status{font-weight:bold}
#banner{margin:24px auto 0;max-width:760px;padding:16px;border-radius:10px;
        font-size:18px;background:#0a8f55}
#banner.WARNING{background:#c98a00}
#banner.CRITICAL{background:#d62d2d}
#advice{display:none;margin:18px auto 0;max-width:760px;padding:18px;text-align:left;
        border-radius:12px;background:#14284a;border:2px solid #13a8b8}
#advice h2{margin:0 0 6px;font-size:22px}
#advice .src{font-size:12px;color:#8fb3c9;margin-bottom:10px}
#advice ul{margin:8px 0 12px 20px;padding:0}
#contact{background:#0b1a2e;border-radius:10px;padding:12px;margin-top:10px}
#contact .name{font-size:20px;font-weight:bold}
#contact .phone{font-size:26px;font-weight:bold;color:#7fdce6}
</style></head><body>
<h1>HVAC Health Monitor</h1>
<div class="sub">Real-time smart system diagnostics</div>
<div class="cards">
  <div class="card" id="c-pressure"><div class="label">AIRFLOW (PRESSURE)</div>
    <div class="value" id="v-pressure">--</div>
    <div class="status" id="s-pressure">--</div></div>
  <div class="card" id="c-temp"><div class="label">TEMPERATURE</div>
    <div class="value" id="v-temp">--</div>
    <div class="status" id="s-temp">--</div></div>
  <div class="card" id="c-vib"><div class="label">VIBRATION</div>
    <div class="value" id="v-vib">--</div>
    <div class="status" id="s-vib">--</div></div>
</div>
<div id="banner">Connecting...</div>
<div id="advice">
  <h2 id="a-head"></h2>
  <div class="src" id="a-src"></div>
  <div id="a-expl"></div>
  <ul id="a-actions"></ul>
  <div id="a-urg"></div>
  <div id="contact">
    <div class="label">WHO TO CONTACT</div>
    <div class="name" id="t-name"></div>
    <div class="phone" id="t-phone"></div>
    <div id="t-note"></div>
  </div>
</div>
<script>
function setCard(name, text, status) {
  document.getElementById('c-' + name).className = 'card ' + status;
  document.getElementById('v-' + name).textContent = text;
  document.getElementById('s-' + name).textContent = status;
}
function showAdvice(d) {
  const box = document.getElementById('advice');
  if (d.overall === 'NORMAL' || !d.advice || !d.advice.headline) { box.style.display = 'none'; return; }
  const a = d.advice;
  box.style.display = 'block';
  document.getElementById('a-head').textContent = a.headline;
  document.getElementById('a-src').textContent = 'Advice source: ' + a.source;
  document.getElementById('a-expl').textContent = a.explanation;
  const ul = document.getElementById('a-actions');
  ul.innerHTML = '';
  (a.actions || []).forEach(x => { const li = document.createElement('li'); li.textContent = x; ul.appendChild(li); });
  document.getElementById('a-urg').textContent = a.urgency ? 'Urgency: ' + a.urgency : '';
  const t = a.technician;
  document.getElementById('contact').style.display = t ? 'block' : 'none';
  if (t) {
    document.getElementById('t-name').textContent = t.name;
    document.getElementById('t-phone').textContent = t.phone;
    document.getElementById('t-note').textContent = t.note || '';
  }
}
async function tick() {
  try {
    const d = await (await fetch('/api/status')).json();
    setCard('pressure', d.pressure_pa === null ? '--' : d.pressure_pa.toFixed(0) + ' Pa',
            d.pressure_status);
    setCard('temp', d.temp_c === null ? '--' : d.temp_c.toFixed(1) + ' °C', d.temp_status);
    setCard('vib', d.vib_events + ' pulses', d.vib_status);
    const b = document.getElementById('banner');
    b.className = d.overall;
    b.textContent = d.alerts.length ? d.alerts.join('  |  ') : 'System healthy. No alerts.';
    showAdvice(d);
  } catch (e) {
    document.getElementById('banner').textContent = 'Connection lost...';
  }
}
setInterval(tick, 1000);
tick();
</script></body></html>"""


@app.route("/")
def index():
    return PAGE


@app.route("/api/status")
def api_status():
    return jsonify(state)


@app.route("/api/technicians")
def api_technicians():
    return jsonify(advisor.load_technicians())


@app.route("/sim/<name>/<value>")
def sim_control(name, value):
    """Simulation mode only: /sim/temp/45   /sim/pressure/900   /sim/vib/12   /sim/temp/off"""
    if not sim.SIMULATE or name not in sim.SIM:
        abort(404)
    sim.SIM[name] = None if value == "off" else float(value)
    return "ok"


if __name__ == "__main__":
    threading.Thread(target=sensor_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
