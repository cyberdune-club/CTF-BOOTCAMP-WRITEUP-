CYBERDUNE RNG/CBC Challenge
===========================

You get a single file: flag.txt.crs
First 16 bytes = IV, rest = AES-CBC ciphertext.

Hints:
- The encryption wasn't just AES. There are *multiple* XOR passes driven by PRNGs.
- One PRNG is a custom 32‑bit xorshift-ish thing with state (x,y,z,w) and weird reseeding.
- Another PRNG is MSVCRT's rand() LCG. Its seed is one of the internal state words above.
- The correct MSVCRT seed can be identified by regenerating (key, iv) and matching the file IV.
- Pipeline (decryption): AES-CBC → PKCS#7 unpad → XOR with pass2 → XOR with pass1 → plaintext.
- The original size isn't stored, so try all 1..16 pad lengths as guesses.
- Verify your streams by checking that IV you derive matches the file's first 16 bytes.

File format:
- [0x00:0x10]  IV (must match PRNG‑derived IV)
- [0x10: ]     AES-CBC ciphertext of padded(pass3)

Deliverables to submit:
- flag (ASCII): starts with CYBERDUNE{...}

Good luck 💫
