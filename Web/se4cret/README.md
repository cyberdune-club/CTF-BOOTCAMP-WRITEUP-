# CYBERDUNE Web Challenge (port 31347)

A lightweight, Docker-ready web CTF challenge with a vulnerable message board and a **report-to-admin** flow.
An internal headless admin bot reviews reported posts using a real Chromium (Puppeteer). The admin's browser
has a non-HttpOnly cookie that contains the flag.

- **Flag format:** `CYBERDUNE{...}`
- **Default port:** `31347`
- **Default flag file:** `flag.txt` (or override with `-e FLAG=...`)

## Run (Docker)

```bash
# Build
docker build -t cyberdune-31347 ./

# Run (maps host :31347 -> container :31347)
docker run -d --name cyberdune-31347 -p 31347:31347 cyberdune-31347

# Or run with a custom flag via env
docker run -d --name cyberdune-31347 -p 31347:31347 -e FLAG="CYBERDUNE{3xUJNV_2V_XQZjQQttvTtcZpIipfT9YnDXV1S9fG}" cyberdune-31347
```

Then open: <http://localhost:31347/>

## Goal

Trigger a stored XSS in a message so that when the **admin bot** opens it, your JavaScript exfiltrates
the admin's cookies (which include the flag) to the `/collect` endpoint. You can then read it at `/logs`.

## Hints

- HTML input is sanitized, but only `<script>...</script>` tags are stripped.
- Event handlers like `onerror`, `onload`, and SVG-based payloads may still execute.
- The admin cookie **is not HttpOnly** (intentionally).

## Example payload

```html
<img src=x onerror="fetch('/collect?d='+encodeURIComponent(document.cookie))">
```

Steps:

1. Post the payload on `/`.
2. Click **Report to admin** next to your message.
3. Wait a second or two, then open `/logs` — you should see the admin's cookies containing the flag.

## Files

- `server.js` – Express app, vulnerable board, `/collect` logger, and headless admin bot.
- `Dockerfile` – Based on Puppeteer's official image; listens on port 31347.
- `package.json` – Dependencies.
- `flag.txt` – Holds the default flag (if `FLAG` env not provided).
- `solve/solve.py` – Automated solver that demonstrates the attack.

## Healthcheck

Container exposes `/health` returning `200 OK` when the server is up.

---

Happy hacking!