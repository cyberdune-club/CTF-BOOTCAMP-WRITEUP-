# serve.py
import socket
import threading
import os
import secrets
from chall import xor_bytes, split_flag, make_primes_for, unstable_pair

HOST = "0.0.0.0"
PORT = int(os.environ.get("SERVICE_PORT", 32548))
FLAG_PATH = "flag.txt"

def load_flag():
    with open(FLAG_PATH, "rb") as f:
        return f.read().strip()

def produce_output_for_connection(flag_bytes):
    # generate fresh primes and pads per connection
    myprime, primes = make_primes_for(myprime_bits=128, other_bits=256)
    p1, p2, p3, p4 = primes

    xor_key = secrets.randbelow(126)
    pad1_byte = secrets.randbelow(126)
    pad2_byte = secrets.randbelow(126)

    enc_flag = xor_bytes(flag_bytes, xor_key)
    fl, ag = split_flag(enc_flag)

    n1, ct1, ct2 = unstable_pair(fl, p1, p2, myprime, 1, pad1_byte)
    n2, ct3, ct4 = unstable_pair(ag, p3, p4, myprime, 2, pad2_byte)

    out = []
    out.append(f"n1 = {n1}")
    out.append(f"ct1 = {ct1}")
    out.append(f"ct2 = {ct2}")
    out.append("")
    out.append(f"n2 = {n2}")
    out.append(f"ct3 = {ct3}")
    out.append(f"ct4 = {ct4}")
    out.append("")
    return "\n".join(out).encode()

def handle_client(conn, addr, flag_bytes):
    try:
        conn.settimeout(10)
        payload = produce_output_for_connection(flag_bytes)
        conn.sendall(payload)
    except Exception:
        try:
            conn.sendall(b"Error\n")
        except Exception:
            pass
    finally:
        try:
            conn.close()
        except Exception:
            pass

def run_server():
    flag = load_flag()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(512)
    print(f"[+] Listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = sock.accept()
            # spawn a daemon thread to handle client so it won't block shutdown
            t = threading.Thread(target=handle_client, args=(conn, addr, flag), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("[+] Shutting down server")
    finally:
        sock.close()

if __name__ == "__main__":
    run_server()

