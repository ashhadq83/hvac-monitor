"""advisor.py - explains the problem and picks who to contact.
Uses the Anthropic API (Claude) when ANTHROPIC_API_KEY is set and the internet works.
Otherwise it falls back to built-in rules, so the dashboard always shows something.
The AI may only choose a contact from technicians.json. It never invents phone numbers."""
import json
import os
import threading
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.environ.get("ADVISOR_MODEL", "claude-haiku-4-5-20251001")
MIN_SECONDS_BETWEEN_CALLS = 20

advice = {"source": "none", "headline": "All systems normal", "explanation": "",
          "actions": [], "urgency": "", "technician": None}
_state = {"signature": None, "busy": False, "last_call": 0.0}


def load_env():
    """Read KEY=VALUE lines from a .env file next to this script (not committed to git)."""
    path = os.path.join(HERE, ".env")
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def load_technicians():
    try:
        with open(os.path.join(HERE, "technicians.json")) as f:
            return json.load(f)
    except Exception:
        return []


RULES = {
    "pressure": ("Airflow restriction detected",
                 "The pressure reading changed a lot, which usually means a clogged filter or a blocked duct or vent.",
                 ["Turn the system off if it is critical", "Check and replace the air filter", "Make sure vents are open and clear"],
                 "airflow"),
    "temperature": ("Temperature outside the normal range",
                    "The air temperature is too high or too low, so the system may be running inefficiently.",
                    ["Check the thermostat settings", "Check the filter and vents", "Book a technician to check the system"],
                    "heating_cooling"),
    "vibration": ("Excess vibration detected",
                  "Strong vibration often points to a worn fan bearing, an unbalanced fan or a loose mount.",
                  ["Turn the unit off if it is shaking hard", "Look for loose panels or mounts", "Book maintenance soon"],
                  "motor_fan"),
}


def pick_technician(specialty, techs, wanted_id=None):
    for t in techs:
        if wanted_id and t.get("id") == wanted_id:
            return t
    for t in techs:
        if specialty in t.get("specialties", []):
            return t
    return techs[0] if techs else None


def fallback_advice(problems, techs):
    worst = max(problems, key=lambda p: (p["status"] == "CRITICAL", p["sensor"] == "pressure"))
    head, expl, actions, spec = RULES[worst["sensor"]]
    if len(problems) > 1:
        head = "Multiple problems detected"
        expl = " ".join(RULES[p["sensor"]][1] for p in problems)
    urgency = "now" if any(p["status"] == "CRITICAL" for p in problems) else "this week"
    return {"source": "offline rules", "headline": head, "explanation": expl, "actions": actions,
            "urgency": urgency, "technician": pick_technician(spec, techs)}


def _ask_claude(problems, techs):
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        raise RuntimeError("no API key")
    system = ("You are an HVAC diagnostics assistant inside a small demo monitor. "
              "Reply with JSON only, no other text, using these keys: "
              "headline (max 10 words), explanation (max 35 words, plain language), "
              "actions (list of at most 3 short strings), urgency (one of: now, today, this week), "
              "technician_id (must be one of the ids in the technician list). "
              "Never invent contact details.")
    user = json.dumps({"readings_with_problems": problems,
                       "technicians": [{"id": t["id"], "name": t["name"], "specialties": t["specialties"],
                                        "note": t.get("note", "")} for t in techs]})
    body = json.dumps({"model": MODEL, "max_tokens": 400, "system": system,
                       "messages": [{"role": "user", "content": user}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST",
                                 headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                                          "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode())
    return parse_reply("".join(b.get("text", "") for b in data.get("content", [])), problems, techs)


def parse_reply(text, problems, techs):
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):]
    obj = json.loads(text[text.find("{"): text.rfind("}") + 1])
    spec = RULES[problems[0]["sensor"]][3]
    return {"source": "AI (Claude)", "headline": str(obj.get("headline", ""))[:120],
            "explanation": str(obj.get("explanation", ""))[:400],
            "actions": [str(a)[:140] for a in obj.get("actions", [])][:3],
            "urgency": str(obj.get("urgency", ""))[:20],
            "technician": pick_technician(spec, techs, obj.get("technician_id"))}


def _worker(problems):
    global advice
    techs = load_technicians()
    try:
        result = _ask_claude(problems, techs)
    except Exception:
        result = fallback_advice(problems, techs)
    advice = result
    _state["busy"] = False


def update(problems):
    """Call every second from the main loop. problems = list of dicts with sensor, status, message, value."""
    global advice
    if not problems:
        _state["signature"] = None
        advice = {"source": "none", "headline": "All systems normal", "explanation": "",
                  "actions": [], "urgency": "", "technician": None}
        return
    sig = tuple(sorted((p["sensor"], p["status"]) for p in problems))
    if sig == _state["signature"] or _state["busy"]:
        return
    if time.time() - _state["last_call"] < MIN_SECONDS_BETWEEN_CALLS:
        advice = fallback_advice(problems, load_technicians())   # instant answer while we wait
        return
    _state["signature"] = sig
    _state["busy"] = True
    _state["last_call"] = time.time()
    advice = fallback_advice(problems, load_technicians())       # show something immediately
    threading.Thread(target=_worker, args=(problems,), daemon=True).start()
