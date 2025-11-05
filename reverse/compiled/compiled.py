# reverse_313.py
STORED = [205, 96, 247, 8, 225, 15, 65, 72, 64, 6, 28, 248, 135, 28, 81, 16, 148, 37, 210, 121, 54, 114, 203, 180]

def ror8(v, r):
    r &= 7
    return ((v >> r) | ((v << (8 - r)) & 0xFF)) & 0xFF

def reverse_transform(stored):
    out_bytes = []
    for i, x in enumerate(stored):
        r = (3 * i + 1) % 8
        b = ror8(x, r)             # inverse rotate
        b = (b - (i * 7)) & 0xFF   # inverse add i*7
        b = b ^ 0xA5               # inverse xor
        b = (b - i) & 0xFF         # inverse add i
        out_bytes.append(b)
    return bytes(out_bytes)

flag_bytes = reverse_transform(STORED)
try:
    flag = flag_bytes.decode('utf-8')
except UnicodeDecodeError:
    flag = flag_bytes

print("Recovered flag:", flag)
