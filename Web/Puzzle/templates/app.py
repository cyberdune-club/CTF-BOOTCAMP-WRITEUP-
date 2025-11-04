
from flask import Flask, request, render_template, make_response
import ipaddress
import os

app = Flask(__name__)

# Load flag from file (better for containerized deploys)
FLAG_PATH = os.environ.get("FLAG_PATH", "flag.txt")

def _client_ip():
    # ❌ VULNERABLE: trusts user-supplied header without a trusted proxy in front
    # If a reverse proxy (nginx) were present, this would be okay **only** if we verified
    # it was set by that proxy. Here we accept it blindly — classic CTF gotcha.
    xfwd = request.headers.get("X-Forwarded-For")
    if xfwd:
        # In case of a chain, take the first value (client)
        ip = xfwd.split(",")[0].strip()
        return ip
    return request.remote_addr or "0.0.0.0"

def _is_loopback(ip_str):
    try:
        return ipaddress.ip_address(ip_str).is_loopback
    except ValueError:
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/whoami")
def whoami():
    # Helper to see what the app thinks your IP is
    cip = _client_ip()
    return {"client_ip": cip, "is_loopback": _is_loopback(cip)}, 200

@app.route("/robots.txt")
def robots():
    resp = make_response("User-agent: *\nDisallow: /admin\nAllow: /whoami\n")
    resp.headers["Content-Type"] = "text/plain"
    return resp

@app.route("/healthz")
def healthz():
    return {"ok": True}, 200

@app.route("/admin")
def admin():
    cip = _client_ip()
    if not _is_loopback(cip):
        return {"error": "admin only from 127.0.0.1"}, 403
    # Read the flag from disk
    try:
        with open(FLAG_PATH, "r", encoding="utf-8") as f:
            flag = f.read().strip()
    except Exception:
        flag = "CYBERDUNE{MISSING_FLAG_FILE}"
    return {"flag": flag, "hint": "proxies can rewrite client IPs…"}, 200

if __name__ == "__main__":
    # Bind to 0.0.0.0 so it can be reached externally; default port 31346 as requested
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "31346")))
