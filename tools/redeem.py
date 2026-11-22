"""Bind a serial number to one Machine ID. Prints 'RESULT: <CODE> - text' (read by SPD)."""
import json, os, re, hashlib, datetime, sys

def out(code, text):
    print(f"RESULT: {code} - {text}")
    sys.exit(0)

body = os.environ.get("BODY", "")
m = re.search(r"```json\s*(\{.*?\})\s*```", body, re.S)
if not m: out("INVALID", "request could not be read")
try: req = json.loads(m.group(1))
except Exception: out("INVALID", "request could not be read")
app = re.sub(r"[^a-z0-9]", "", str(req.get("app", "spd")).lower()) or "spd"
mid = str(req.get("id", "")).strip().upper()
serial = re.sub(r"[^A-Z0-9]", "", str(req.get("serial", "")).upper())
if not re.fullmatch(r"[A-Z]+-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}", mid): out("INVALID", "bad Machine ID")
if len(serial) < 16: out("INVALID", "serial number is not valid")
h = hashlib.sha256(serial.encode()).hexdigest()

path = f"licenses/{app}.json"
data = json.load(open(path, encoding="utf-8"))
ser = next((s for s in data.get("serials", []) if s.get("hash", "").lower() == h), None)
if ser is None: out("INVALID", "serial number is not valid")
if ser.get("revoked"): out("INVALID", "serial number was cancelled")
used = str(ser.get("used_by", "")).upper()
if used and used != mid: out("USED", "this serial number is already used on another PC")

# count from the moment the serial is pasted, by Dubai date (runner clock is UTC)
today = (datetime.datetime.utcnow() + datetime.timedelta(hours=4)).date()
days = int(ser.get("days") or 0)
machines = data.setdefault("machines", [])
pc = next((x for x in machines if str(x.get("id", "")).upper() == mid), None)
if used == mid and pc and pc.get("serial") == ser.get("hint"):
    out("OK", "already activated on this PC" + (f" until {pc['expires']}" if pc.get("expires") else ""))
expires = (today + datetime.timedelta(days=days)).isoformat() if days > 0 else ""
name = f"{req.get('pc', 'PC')} / {req.get('user', '')}".strip(" /")
entry = {"id": mid, "name": name, "status": "allow", "expires": expires, "serial": ser.get("hint", "")}
if pc: pc.clear(); pc.update(entry)
else: machines.append(entry)
ser["used_by"] = mid; ser["used_on"] = today.isoformat(); ser["used_pc"] = name
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False); f.write("\n")
out("OK", "activated" + (f" until {expires}" if expires else " (no expiry)"))
