import re
key = b"M0R0CC0_CTF"

def xor_decrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

# تأكد من وجود dump.bin
try:
    data = open("dump.bin", "rb").read()
except FileNotFoundError:
    print("ERROR: dump.bin not found. Run: base64 -d dump.b64 > dump.bin")
    raise SystemExit(1)

matches = list(re.finditer(rb"<<OFFSET_([0-9a-fA-F]+)>>([0-9a-fA-F]+)<<END>>", data))
print(f"[+] Found {len(matches)} fragments")

fragments = []
for m in matches:
    offset = int(m.group(1), 16)
    hexdata = m.group(2)
    try:
        dec = xor_decrypt(bytes.fromhex(hexdata.decode()), key)
    except Exception as e:
        print(f"[-] Error decoding fragment at offset 0x{offset:x}: {e}")
        continue
    fragments.append((offset, dec))

if not fragments:
    print("[-] No fragments decrypted. Try: strings dump.bin | grep OFFSET")
    raise SystemExit(1)

fragments.sort(key=lambda x: x[0])
flag = b''.join([f[1] for f in fragments])

print("\n[+] Decrypted fragments (in offset order):")
for off, part in fragments:
    print(f"  0x{off:08x} -> {part}")

print("\n[+] Stitched flag:", flag.decode(errors='ignore'))
