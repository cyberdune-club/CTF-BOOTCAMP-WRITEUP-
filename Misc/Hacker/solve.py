#!/usr/bin/env python3
import socket, sys, time

HOST = "159.223.23.56"
PORT = 31345

def recv_until(sock, term=b": ", timeout=5.0):
    sock.settimeout(timeout)
    data = b""
    try:
        while not data.endswith(term):
            chunk = sock.recv(4096)
            if not chunk: break
            data += chunk
    except socket.timeout: pass
    return data

def make_pairs(n):
    pairs, used, i = [], set(), 1
    while len(pairs) < n:
        a = str(i)
        b = a + "9"
        if a.endswith("9") or a in used or b in used:
            i += 1
            continue
        pairs.append((a, b))
        used.add(a); used.add(b)
        i += 1
    return pairs

def run(host=HOST, port=PORT):
    pairs = make_pairs(100)
    print(f"[+] Prepared {len(pairs)} pairs. Connecting {host}:{port} ...")
    with socket.create_connection((host, port), timeout=10) as s:
        recv_until(s, b"Enter first number: ")
        for a, b in pairs:
            s.sendall((a+"\n").encode())
            recv_until(s, b"Enter second number: ")
            s.sendall((b+"\n").encode())
            recv_until(s, b"Enter first number: ", timeout=2.5)
        # Read flag
        time.sleep(0.2)
        try:
            while True:
                s.settimeout(0.5)
                chunk = s.recv(4096)
                if not chunk: break
break
                sys.stdout.buffer.write(chunk); sys.stdout.flush()
        except socket.timeout: pass

if name == "main":
    run()
