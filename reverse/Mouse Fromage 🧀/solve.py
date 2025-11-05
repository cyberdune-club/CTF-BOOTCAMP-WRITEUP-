#!/usr/bin/env python3
import binascii
from dataclasses import dataclass
from typing import Tuple, Optional
from Crypto.Cipher import AES

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
    for _ in range(orig_size):
        key_byte = randd(state) & 0xFF
        out[_] = key_byte
        ssrand(state, randd(state))  
    return state, bytes(out)

def generate_pass2_and_key_iv(seed: int, length: int) -> Tuple[bytes, bytes, bytes]:
    cr = MSVCRTRand(seed)
    p2 = bytearray(length)
    for i in range(length):
        p2[i] = cr.rand() & 0xFF
    _ = cr.rand()
    key = bytearray(32)
    for i in range(32):
        key[i] = (cr.rand() ^ 0x2025) & 0xFF
    iv = bytearray(16)
    for i in range(16):
        iv[i] = (cr.rand() ^ 0x1337) & 0xFF
    return bytes(p2), bytes(key), bytes(iv)

def try_decrypt(aes_encrypted: bytes, file_iv: bytes) -> Optional[str]:
    enc_len = len(aes_encrypted)
    for pad_guess in range(1, 17):
        orig_size = enc_len - pad_guess
        if orig_size <= 0:
            continue
        state_after_p1, p1_stream = simulate_pass1_get_state_and_stream(orig_size)
        seeds = [state_after_p1.x, state_after_p1.y, state_after_p1.z, state_after_p1.w]
        for seed in seeds:
            p2_stream, key, iv = generate_pass2_and_key_iv(seed, orig_size)
            if iv != file_iv:
                continue
            cipher = AES.new(key, AES.MODE_CBC, file_iv)
            pass3_plain = pkcs7_unpad(cipher.decrypt(aes_encrypted))
            pass3_plain = pass3_plain[:orig_size]
            inter = xor_bytes(pass3_plain, p2_stream)
            plaintext = xor_bytes(inter, p1_stream)
            try:
                return plaintext.decode('ascii', errors='strict')
            except UnicodeDecodeError:
                return plaintext.decode('latin1')
    return None

def main():
    with open("flag.txt.crs", "rb") as f:
        data = f.read()
    file_iv = data[:16]
    aes_encrypted = data[16:]
    print(f"IV from file: {binascii.hexlify(file_iv).decode().upper()}")
    print(f"Encrypted data size: {len(aes_encrypted)} bytes")
    result = try_decrypt(aes_encrypted, file_iv)
    if result is None:
        print("✗ Could not decrypt")
    else:
        print("✓ FLAG:", result)

if __name__ == "__main__":
    main()
