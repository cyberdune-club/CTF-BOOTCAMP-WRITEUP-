
# CYBERDUNE Web Challenge Puzzle

A tiny Flask challenge: the `/admin` endpoint is restricted to localhost, **but** the app naively
trusts `X-Forwarded-For`. Spoof that header to appear as `127.0.0.1` and grab the flag.

## Flag format
`CYBERDUNE{SPOOFED_PROXY_IP_WINS}` (you can change it in `flag.txt`).

## Quick start (bare metal)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
# listens on 0.0.0.0:31346
```

## Docker

```bash
docker build -t cyberdune-web .
docker run --rm -p 31346:31346 -e FLAG_PATH=/app/flag.txt cyberdune-web
```

## Deploy on your VPS (port 31346)

If you already have Docker:

```bash
scp -P <ssh_port> cyberdune_web_challenge.zip user@vps:/tmp/
ssh -p <ssh_port> user@vps 'unzip -o /tmp/cyberdune_web_challenge.zip -d ~/cyberdune && cd ~/cyberdune && docker build -t cyberdune-web . && docker run -d --name cyberdune -p 31346:31346 -e FLAG_PATH=/app/flag.txt cyberdune-web'
```

Then visit: `http://<your_vps_ip>:31346/`

## Intended solution

Send `X-Forwarded-For: 127.0.0.1` with your request to `/admin`.

Example with curl:

```bash
curl -s -H 'X-Forwarded-For: 127.0.0.1' http://<host>:31346/admin
```

or run `solve.py` in this directory.
