# solve_lost.py
stored = [
    25,14,176,57,130,198,202,64,158,116,146,212,43,165,153,240,
    217,251,24,181,35,209,151,131,117,29,153,179,216,167,99,252
]

def ror8(v, r):
    r &= 7
    return ((v >> r) | ((v << (8 - r)) & 0xFF)) & 0xFF

out = []
for i, x in enumerate(stored):
    r = i % 7                      # inverse of rol(b, i % 7)
    b = ror8(x, r)                 # right rotate by r
    b = (b - ((i * 7) % 256)) & 0xFF
    b = b ^ 0x5A
    b = (b - (i & 0xFF)) & 0xFF
    out.append(b)

flag = bytes(out)
try:
    print("Recovered flag:", flag.decode('utf-8'))
except:
    print("Recovered bytes:", flag)
