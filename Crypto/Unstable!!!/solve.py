#!/usr/bin/env python3
# recover.py
# Reproduce the steps to recover the flag from the challenge ciphertexts.

from math import isqrt, gcd
from typing import Tuple, Optional


# challenge values (paste directly from the challenge)
n1 = 3200410225089768253393204908495231504462430605270198310102814054852129335792233415359102891140
ct1 = 3254762955123908704476292606609658298352903947011632752350438470834430068182418854942149087461
ct2 = 2713761205775414305531185925769077078637582638213880848463026056075680865592663396684070346429

n2 = 4824784152838780781628628048358029638529886113933771938735038637814889595763839377567032719495
ct3 = 6524319654353549487789580058525863762815413497375167057532560674204667096523104036378129624333
ct4 = 3831520375938884041029389873933140913754198564563401360361419435736794736946692701050177908904


def compute_shared_prime(n1: int, n2: int) -> int:
    """
    Compute g = gcd(n1-4, n2-4), then return myprime = g // 3.
    Raises SystemExit if g not divisible by 3.
    """
    g = gcd(n1 - 4, n2 - 4)
    if g % 3 != 0:
        raise SystemExit("unexpected: g not divisible by 3")
    myprime = g // 3
    return myprime


def recover_m(ct: int, myprime: int) -> int:
    """
    Solve m^2 + myprime*m - ct = 0 for positive integer m.
    Uses integer square root; raises ValueError if discriminant is not a perfect square.
    Returns the positive root.
    """
    D = myprime * myprime + 4 * ct
    s = isqrt(D)
    if s * s != D:
        raise ValueError("Discriminant not a perfect square for ct=%d" % ct)
    # m = (-myprime + s) // 2  (we expect this to be integer and positive)
    m = (-myprime + s) // 2
    if m <= 0:
        raise ValueError("Recovered m is non-positive for ct=%d" % ct)
    return m


def int_to_bytes(n: int) -> bytes:
    """
    Convert an integer to big-endian bytes; returns b'' for n == 0.
    """
    if n == 0:
        return b''
    bl = (n.bit_length() + 7) // 8
    return n.to_bytes(bl, 'big')


def single_byte_xor(data: bytes, key: int) -> bytes:
    return bytes([c ^ key for c in data])


def printable_score(bs: bytes) -> float:
    if len(bs) == 0:
        return 0.0
    good = sum(1 for c in bs if 32 <= c <= 126 or c in (9, 10, 13))
    return good / len(bs)


def brute_force_single_byte_key(b1: bytes, b2: bytes) -> Tuple[int, bytes]:
    """
    Brute-force a single-byte XOR key by scoring printable fraction on both halves.
    Returns best_key and decoded bytes (b1+b2) XORed by best_key.
    """
    best = []
    for key in range(256):
        dec1 = single_byte_xor(b1, key)
        dec2 = single_byte_xor(b2, key)
        score = (printable_score(dec1) + printable_score(dec2)) / 2
        best.append((score, key, dec1, dec2))
    best.sort(reverse=True, key=lambda x: x[0])
    best_score, best_key, best_dec1, best_dec2 = best[0]
    dec_full = single_byte_xor(b1 + b2, best_key)
    return best_key, dec_full


def pretty_print_bytes(bs: bytes) -> None:
    print("hex:", bs.hex())
    try:
        print("ascii:", bs.decode('utf-8'))
    except UnicodeDecodeError:
        print("ascii: (utf-8 decode failed)")


def main():
    print("1) computing shared prime from n1, n2...")
    myprime = compute_shared_prime(n1, n2)
    print("myprime =", myprime)

    print("\n2) recovering m for ct1 and ct2...")
    try:
        m1 = recover_m(ct1, myprime)
        m2 = recover_m(ct2, myprime)
    except ValueError as e:
        raise SystemExit(f"error recovering m: {e}")

    print("m1 bitlength:", m1.bit_length())
    print("m2 bitlength:", m2.bit_length())

    b1 = int_to_bytes(m1)
    b2 = int_to_bytes(m2)
    print("len b1, b2:", len(b1), len(b2))
    print("b1 (hex):", b1.hex())
    print("b2 (hex):", b2.hex())

    print("\n3) brute-forcing single-byte XOR key...")
    best_key, dec_full = brute_force_single_byte_key(b1, b2)
    print("best_key:", best_key)
    print("\ndecoded (full) ->")
    pretty_print_bytes(dec_full)

    # show top candidates (optional, helpful for manual inspection)
    print("\n(If output looks wrong, consider printing top few key candidates manually.)")


if __name__ == "__main__":
    main()
