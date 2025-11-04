#!/usr/bin/env python3
import random
from Crypto.Util.number import getPrime

def generate_rsa_keys():
    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    e = random.choice([3,5,7,11,13,17])
    return n, e

def get_ciphertext():
    try:
        with open("flag.txt", "rb") as f:
            data = f.read().strip()
            # المؤلف ديال الـchallenge طبّع مباشرة integer representation
            return int.from_bytes(data, "big")
    except FileNotFoundError:
        print("[ERROR] flag.txt missing!")
        return None

def main():
    print("=== CyberDune RSA Challenge (docker reproducible) ===")
    n, e = generate_rsa_keys()
    print(f"N = {n}")
    print(f"e = {e}")
    ct = get_ciphertext()
    if ct:
        print(f"Encrypted flag: {ct}")
    print("Good luck!")

if __name__ == "__main__":
    main()
