#!/usr/bin/env python3
# solve.py -- Automatically decodes mystery.enc and prints the flag.
import sys, zlib, base64

def solve(path):
    s = open(path, 'r').read().strip()
    # 1) reverse
    s = s[::-1]
    # 2) hex -> bytes
    try:
        b = bytes.fromhex(s)
    except Exception as e:
        print('Hex decode failed:', e); return
    # 3) base64 decode
    try:
        comp = base64.b64decode(b)
    except Exception as e:
        print('Base64 decode failed:', e); return
    # 4) decompress zlib
    try:
        flag = zlib.decompress(comp).decode('utf-8')
    except Exception as e:
        print('Decompression failed:', e); return
    print('FLAG:', flag)

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'mystery.enc'
    solve(path)
