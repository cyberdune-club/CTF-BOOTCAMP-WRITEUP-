# CTF Write-up: Fl1pper Zer0

**Challenge:** Fl1pper Zer0
**Category:** Cryptography
**Difficulty:** Medium
**Points:** 500
**Solver:** valague
**Date:** 03/11/2025

---

## My Journey Solving This Challenge

### 1. First impressions

When I first connected to the service I saw:

```
Welcome to Fl1pper Zer0 – Signing Service!
Here is your encrypted signing key, use it to sign a message :
{
  "pubkey": {
    "x": "0xb5b8c9d3cd2ce971952bcff3ea648f4fae9d361928c48fa41d1f6b99dec981a4",
    "y": "0xc714db9d13e898dcbc278cf83274a7f109a8f463729e4a0ab8f121fd85aefc21"
  },
  "signkey": "4f7d46d579ff717115ce52333afcc8910b69cb0fe494544293e922193ee76adf0d07c7e361648f874057e387506dcdcb"
}
```

The `"signkey"` looked like encrypted data and a public key was provided. I decided to explore the service functionality.

---

### 2. Understanding the service

I generated a new key to see the behavior:

**Sent:**

```json
{"option": "generate_key"}
```

**Received:**

```json
{
  "pubkey": {
    "x": "0x377984d527b5bdf279b09bb83b20e7578109738b01a19f23530850015ea4f955",
    "y": "0xc086bd09b15633a39d40deab0b44ad262649eb7837081396810c173fb854f96b"
  },
  "signkey": "5860e43822a2b22af1b74ca8951c9e62aa479e5b09df3e2bcb7b0c85e6cc137e1c3972a955cd790ab7190c30b15ac93b"
}
```

The `signkey` changed; it appeared to be an encrypted representation of the private key.

---

### 3. Testing the signing function

I signed the message `"hello"` (hex `68656c6c6f`) using the new `signkey`:

**Sent:**

```json
{"option": "sign", "msg": "68656c6c6f", "signkey": "5860e43822a2b22af1b74ca8951c9e62aa479e5b09df3e2bcb7b0c85e6cc137e1c3972a955cd790ab7190c30b15ac93b"}
```

**Received:**

```json
{"r": "0x48ebe1fec71baf3777b4cebd897c3fe21a74871747a995b8eb615d8f96c601",
 "s": "0x7d6e130626f13de16c0ccffa229c8cfb0bce495d593414f39ace22d2e227e520"}
```

This returned `r` and `s` values — an ECDSA signature.

---

### 4. The “Aha!” moment

I remembered ECDSA nonce reuse vulnerabilities. I signed a second message, `"world"` (hex `776f726c64`), with the same `signkey`:

**Sent:**

```json
{"option": "sign", "msg": "776f726c64", "signkey": "5860e43822a2b22af1b74ca8951c9e62aa479e5b09df3e2bcb7b0c85e6cc137e1c3972a955cd790ab7190c30b15ac93b"}
```

**Received:**

```json
{"r": "0x48ebe1fec71baf3777b4cebd897c3fe21a74871747a995b8eb615d8f96c601",
 "s": "0xfdcf6c4f24606c23175464afb3e61d0ff0a9ae49906236d73c83817a1358ada4"}
```

`r` was identical for both signatures — nonce reuse confirmed.

---

### 5. The math (brief)

For ECDSA:

* `r` is derived from the random nonce `k`.
* `s` depends on `k`, the message hash `z`, and the private key `d`.

If the same `k` is used for two different messages:

```
k = (z1 - z2) * (s1 - s2)^{-1}  (mod n)
d = (s1 * k - z1) * r^{-1}      (mod n)
```

---

### 6. Exploit implementation (Python)

```python
from hashlib import sha256

# Curve order for NIST P-256
n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

# Captured values
r = 0x48ebe1fec71baf3777b4cebd897c3fe21a74871747a995b8eb615d8f96c601
s1 = 0x7d6e130626f13de16c0ccffa229c8cfb0bce495d593414f39ace22d2e227e520
s2 = 0xfdcf6c4f24606c23175464afb3e61d0ff0a9ae49906236d73c83817a1358ada4

# Message hashes
z1 = int(sha256(b"hello").hexdigest(), 16)
z2 = int(sha256(b"world").hexdigest(), 16)

# Recover nonce k
k = ((z1 - z2) * pow(s1 - s2, -1, n)) % n
print(f"Recovered k: {k}")

# Recover private key d
d = ((s1 * k - z1) * pow(r, -1, n)) % n
print(f"Recovered private key: {d}")
```

---

### 7. Decrypting the flag

The service returned an encrypted flag (AES). The challenge specified the AES key is `sha256(private_key_bytes)[:16]`.

```python
from Crypto.Cipher import AES
from hashlib import sha256

# Derive AES key from the recovered private key
key = sha256(d.to_bytes(32, 'big')).digest()[:16]

encrypted_flag = bytes.fromhex(
    "0dcb40d82490a044c6e0383e7cb43b4911300f6d10f72ad1376b6643add09dc0b466c593379483249d143a69311994f5a4e3a45e15fb88140fdfaaf07312a9fb9a2b0bc8e3970351b1f06c2b75714bf5"
)

cipher = AES.new(key, AES.MODE_ECB)
flag = cipher.decrypt(encrypted_flag)
print("Flag:", flag.decode())
```

**Recovered flag:**

```
CYBERDUNE{cda8a3f400fdb1a73446cbc7494fbf3420bff9b9d41d4dea97088477cb3285d2}
```

---

### 8. What I learned

* **ECDSA fundamentals:** how signatures use randomness and why it matters.
* **Nonce reuse is catastrophic:** reusing `k` allows private key recovery.
* **Applied modular math:** computing modular inverses and reconstructing keys.
* **Practical cryptography:** combining hash, modular arithmetic, and symmetric decryption.

---

### 9. Challenges I faced

* Understanding why nonce reuse was exploitable.
* Initially using the wrong curve parameters (confused secp256k1 vs NIST P-256).
* Learning modular inverse usage (`pow(x, -1, n)`) and proper big-integer handling.
* Installing/testing the right Python crypto libraries.

---

### 10. Conclusion

Small implementation mistakes in cryptography can completely break security. This challenge was an excellent exercise in identifying nonce reuse, applying the math, and retrieving a real flag. Getting the flag after the whole process was very satisfying and boosted my confidence for future crypto challenges.

---

