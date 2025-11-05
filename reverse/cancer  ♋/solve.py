#!/usr/bin/env python3
import os
import re
import sys
import binascii
from dataclasses import dataclass
from typing import Tuple, Optional
from Crypto.Cipher import AES

FLAG_PATTERN = re.compile(rb"CYBERDUNE\{[^}]{1,400}\}")

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes([x ^ y for x, y in zip(a, b)])

@dataclass
class RNGState:
    x: int = 0x11223344
    y: int = 0xABACADAE
    z: int = 0x1C0DE1C0
    w: int = 0x13372025

def randd(state: RNGState) -> int:
    t = state.x & 0xFFFFFFFF
    t ^= (t << 11) & 0xFFFFFFFF
    t ^= (t >> 8) & 0xFFFFFFFF
    state.x = state.y
    state.y = state.z
    state.z = state.w
    state.w ^= (state.w >> 19) & 0xFFFFFFFF
    state.w ^= t & 0xFFFFFFFF
    result = state.w & 0xFFFFFFFF
    # scramble (mimic original)
    result = (((result >> 16) ^ result) * 0x45D9F3B) & 0xFFFFFFFF
    result = (((result >> 16) ^ result) * 0x3848F357) & 0xFFFFFFFF
    result = ((result >> 16) ^ result) & 0xFFFFFFFF
    return result & 0x7FFFFFFF

def ssrand(state: RNGState, s: int) -> None:
    s &= 0xFFFFFFFF
    state.x = (s ^ 0xF00DABCD) & 0xFFFFFFFF
    state.y = ((s << 16) | (s >> 16)) & 0xFFFFFFFF
    state.z = ((~s) + 0x13371347) & 0xFFFFFFFF
    state.w = (s * 0x9E3779B1) & 0xFFFFFFFF
    for _ in range(19):
        randd(state)

class MSVCRTRand:
    def __init__(self, seed: int) -> None:
        self.srand(seed)
    def srand(self, seed: int) -> None:
        self._state = seed & 0xFFFFFFFF
    def rand(self) -> int:
        self._state = (self._state * 214013 + 2531011) & 0xFFFFFFFF
        return (self._state >> 16) & 0x7FFF

def pkcs7_unpad(data: bytes) -> bytes:
    if not data:
        return data
    pad = data[-1]
    if pad < 1 or pad > 16:
        return data
    if data[-pad:] != bytes([pad]) * pad:
        return data
    return data[:-pad]

def simulate_pass1_get_state_and_stream(orig_size: int) -> Tuple[RNGState, bytes]:
    state = RNGState()
    ssrand(state, orig_size)
    out = bytearray(orig_size)
    for i in range(orig_size):
        key_byte = randd(state) & 0xFF
        out[i] = key_byte
        ssrand(state, randd(state))
    return state, bytes(out)

def generate_pass2_and_key_iv(seed: int, length: int) -> Tuple[bytes, bytes, bytes]:
    cr = MSVCRTRand(seed)
    p2 = bytearray(length)
    for i in range(length):
        p2[i] = cr.rand() & 0xFF
    _ = cr.rand()  # consumed in original sequence
    key = bytearray(32)
    for i in range(32):
        key[i] = (cr.rand() ^ 0x2025) & 0xFF
    iv = bytearray(16)
    for i in range(16):
        iv[i] = (cr.rand() ^ 0x1337) & 0xFF
    return bytes(p2), bytes(key), bytes(iv)

def try_decrypt(aes_encrypted: bytes, file_iv: bytes, verbose: bool = True) -> Optional[bytes]:
    enc_len = len(aes_encrypted)
    attempts = 0
    for pad_guess in range(1, 17):
        orig_size = enc_len - pad_guess
        if orig_size <= 0:
            continue
        state_after_p1, p1_stream = simulate_pass1_get_state_and_stream(orig_size)
        seeds = [state_after_p1.x & 0xFFFFFFFF, state_after_p1.y & 0xFFFFFFFF,
                 state_after_p1.z & 0xFFFFFFFF, state_after_p1.w & 0xFFFFFFFF]
        for seed in seeds:
            attempts += 1
            if verbose and (attempts % 1000 == 0):
                print(f"[+] attempts={attempts}, pad_guess={pad_guess}, trying seed=0x{seed:08X}")
            p2_stream, key, iv = generate_pass2_and_key_iv(seed, orig_size)
            # quick IV check
            if iv != file_iv:
                continue
            # iv matches — attempt full decrypt
            try:
                cipher = AES.new(key, AES.MODE_CBC, file_iv)
                decrypted = cipher.decrypt(aes_encrypted)
            except Exception as e:
                if verbose:
                    print(f"[!] AES decrypt error with seed 0x{seed:08X}: {e}")
                continue
            # remove PKCS7 (this yields the "pass3" plaintext)
            pass3_plain = pkcs7_unpad(decrypted)
            # now trim to supposed original size (pre-padding)
            if len(pass3_plain) < orig_size:
                # unexpected — skip
                continue
            pass3_plain = pass3_plain[:orig_size]
            inter = xor_bytes(pass3_plain, p2_stream)
            plaintext = xor_bytes(inter, p1_stream)
            # check for a flag-looking pattern
            if FLAG_PATTERN.search(plaintext):
                if verbose:
                    print(f"[+] Found candidate with seed 0x{seed:08X}, pad_guess={pad_guess}")
                return plaintext
            # also try decode/text heuristics: printable ratio
            printable = sum(32 <= b < 127 for b in plaintext)
            if printable / max(1, len(plaintext)) > 0.85:
                if verbose:
                    print(f"[+] High-printable candidate (seed=0x{seed:08X}, pad_guess={pad_guess}), saving as candidate.")
                return plaintext
    if verbose:
        print(f"[-] Exhausted search after {attempts} attempts — no candidate matched.")
    return None

def main(fname: str = "flag.txt.crs"):
    if not os.path.isfile(fname):
        print(f"File not found: {fname}")
        return
    data = open(fname, "rb").read()
    if len(data) < 16:
        print("File too small / missing IV.")
        return
    file_iv = data[:16]
    aes_encrypted = data[16:]
    print(f"IV from file: {binascii.hexlify(file_iv).decode().upper()}")
    print(f"Encrypted data size: {len(aes_encrypted)} bytes")
    candidate = try_decrypt(aes_encrypted, file_iv, verbose=True)
    if candidate is None:
        print("\n\u2717 Could not find matching IV/key via RNG reconstruction. Possible causes: wrong rand() variant or corrupted inputs.")
        return
    # try to decode for display
    try:
        text = candidate.decode("utf-8")
    except Exception:
        text = candidate.decode("latin1", errors="replace")
    print("\n\u2713 SUCCESS! Candidate plaintext (first 400 chars):\n")
    print(text[:400])
    outname = "flag_decrypted_candidate.bin"
    with open(outname, "wb") as f:
        f.write(candidate)
    print(f"\nSaved candidate binary to {outname}")
    # quick flag extraction
    m = FLAG_PATTERN.search(candidate)
    if m:
        try:
            print("\nFlag found:", m.group(0).decode())
        except Exception:
            print("\nFlag bytes:", m.group(0))
    else:
        print("\nNo exact CYBERDUNE{...} pattern found inside candidate — inspect the saved file.")

if __name__ == "__main__":
    # allow passing filename as first arg
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
