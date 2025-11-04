#!/usr/bin/env python3
import socket
import threading
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

HOST = '0.0.0.0'
PORT = 1337
KEEP_SECONDS = 180       # خلي الكونكسيون مفتوح 3 دقائق (180s)
MAX_WORKERS = 20         # حد أقصى لعدد الـthreads العاملة باش مايتعطّلش السيرفر

def handle_client(conn, addr):
    try:
        # run enc.py without timeout (will finish quickly in our case)
        p = subprocess.Popen(["python3", "enc.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()  # no timeout
        if out:
            conn.sendall(out)
        if err:
            conn.sendall(b"\n[stderr]\n" + err)
        # keep connection open for KEEP_SECONDS to satisfy "instance stays running"
        # during this time the client remains connected and can observe latency/timing if wanted.
        # if the client disconnects earlier, sending will raise and we'll close.
        try:
            # send a heartbeat newline every 30s to keep NATs alive and show it's still alive
            elapsed = 0
            interval = 30
            while elapsed < KEEP_SECONDS:
                time.sleep(interval)
                elapsed += interval
                try:
                    conn.sendall(b'')  # zero-length attempt to detect closed socket (no data)
                except Exception:
                    break
        except Exception:
            pass
    except Exception as e:
        try:
            conn.sendall(f"[server error] {e}\n".encode())
        except Exception:
            pass
    finally:
        try:
            conn.close()
        except Exception:
            pass

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Listening on {HOST}:{PORT}, keepalive {KEEP_SECONDS}s, max_workers {MAX_WORKERS}")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while True:
            conn, addr = s.accept()
            # submit handler to thread pool
            executor.submit(handle_client, conn, addr)

if __name__ == "__main__":
    main()

