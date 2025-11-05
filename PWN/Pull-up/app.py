#!/usr/bin/env python3
import base64
import socket
import sys
import signal
import os
import mmap
import ctypes
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_REG

HOST = "0.0.0.0"
PORT = 31341

# Exit automatically after 180 seconds (3 minutes)
def on_alarm(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGALRM, on_alarm)
signal.alarm(180)

def check(code: bytes):
    if len(code) > 0x2000:
        return False

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    for insn in md.disasm(code, 0):
        name = insn.insn_name()
        if name != "pop" and name != "push":
            if name == "int3":
                continue
            return False
        # ensure operands exist and first operand is a register
        if not insn.operands or insn.operands[0].type != CS_OP_REG:
            return False

    return True

def run(code: bytes):
    # map RWX memory, write code, and execute it
    size = ((len(code) + 0x1000 - 1) // 0x1000) * 0x1000
    m = mmap.mmap(-1, size, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
    m.write(code)
    # get address of buffer
    addr = ctypes.addressof(ctypes.c_char.from_buffer(m))
    func_type = ctypes.CFUNCTYPE(ctypes.c_int)
    f = func_type(addr)
    try:
        f()
    except Exception as e:
        # swallow exceptions from running native code
        pass

def handle_conn(conn, addr):
    conn.sendall(b"Shellcode : ")
    data = b""
    # read a line (base64)
    while not data.endswith(b"\n"):
        chunk = conn.recv(1024)
        if not chunk:
            break
        data += chunk
        if len(data) > 10 * 1024:
            break
    data = data.strip()
    try:
        code = base64.b64decode(data)
    except Exception as e:
        conn.sendall(b"Invalid base64\n")
        conn.close()
        return

    if not check(code):
        conn.sendall(b"Bad instructions - rejected\n")
        conn.close()
        return

    # Duplicate socket fd to stdin/out/err so a spawned shell uses the network
    fd = conn.fileno()
    os.dup2(fd, 0)
    os.dup2(fd, 1)
    os.dup2(fd, 2)

    # Execute the code
    run(code)

    try:
        conn.sendall(b"\nBye\n")
    except:
        pass
    conn.close()

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)
    # single accept loop; server will exit on SIGALRM after 180s
    while True:
        try:
            conn, addr = srv.accept()
            handle_conn(conn, addr)
        except KeyboardInterrupt:
            break
        except Exception:
            continue

if __name__ == "__main__":
    main()
