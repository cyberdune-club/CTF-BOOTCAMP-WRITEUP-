# enc.py
# Utility used by serve_tcp.py to create rounds that mimic the original challenge behavior.


import random
import gmpy2


def make_round(b):
"""Return tuple (n, a, c, m) where a = m**3 % n and c = (m+1)**3 % n.
b is the parameter used in the original challenge (typically 30*i).
"""
# choose p and q near 2**b like original
p = gmpy2.next_prime(2 ** b + random.randint(0, 2 ** b))
q = gmpy2.next_prime(2 ** b + random.randint(0, 2 ** b))
n = p * q
# original used m = random.randint(0, 4 ** b)
# 4**b == 2**(2*b) so we sample a random integer of approx that many bits
m = random.getrandbits(2 * b)
a = int(gmpy2.powmod(m, 3, n))
c = int(gmpy2.powmod(m + 1, 3, n))
return int(n), a, c, int(m)
