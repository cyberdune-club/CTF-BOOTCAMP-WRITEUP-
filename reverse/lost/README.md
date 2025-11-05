# README.md — lost_chal (Simple C reversing challenge)

## Challenge overview

* **Name:** lost
* **Points:** 499
* **Binary / Source:** `lost_chal.c` (C source supplied)
* **Objective:** Reverse the in-binary transform and recover the secret flag that, when transformed, matches the embedded `stored[]` byte array.

## Summary

This challenge verifies a flag by applying a deterministic, byte-wise transform to each input character and comparing the result to a static `stored[]` array. The transform consists of:

1. Add the index `i` to the byte (`b = b + i`) modulo 256.
2. XOR with `0x5A` (`b ^= 0x5A`).
3. Add `(i*7) % 256` to the byte (`b = b + (i*7)` modulo 256).
4. Rotate-left the byte by `i % 7` bits.

The program rejects inputs of incorrect length and has a `decoy_worker()` function that provokes noise for static analysis but has no impact on the actual gating logic.

## Files

* `lost_chal.c` — challenge source (provided)
* `stored[]` — embedded byte array in the source (length 32)

## Build instructions

To compile locally:

```bash
# Simple build
gcc -o lost_chal lost_chal.c

# With debug symbols (optional)
gcc -g -O0 -o lost_chal_debug lost_chal.c
```

## Reversing approach

Because the transformation is purely byte-wise and reversible, the simplest approach is to invert each operation in reverse order for every `stored[i]`:

* Step 4 inverse (rotate-left by `r`): apply a right-rotate by `r` (i.e., `ror(b, r)`).
* Step 3 inverse (add `(i*7)`): subtract `(i*7)` modulo 256.
* Step 2 inverse (xor `0x5A`): XOR with `0x5A` again (self-inverse).
* Step 1 inverse (add `i`): subtract `i` modulo 256.

After reversing, the result is the original ASCII value for that position in the flag.


## Example output (solution)

Running the solver yields the recovered flag:

```
CYBERDUNE{LOST_FLAG_FOUND_2025>}
```

Note: the flag includes the `>` character inside the braces as shown above; use the exact recovered string when submitting.

## Hints for players

* Ignore the `decoy_worker()` function — it exists solely to confuse static analysis and does not affect the flag check.
* The rotation uses `i % 7`, not `i % 8` (so rotations of 0..6 are used).
* Work per-byte: reversing is local to each position; no global state.

## Hardening notes (for authors)

* Storing secrets in static arrays is trivially reversible. For real applications, never embed secrets in client-side binaries.
* To increase the difficulty for CTF players: spread the transform across multiple translation units, introduce runtime-generated constants pulled from remote servers, or use code virtualization/obfuscation layers.

## Credits

Challenge author: [unspecified]
Difficulty estimate: Easy–Medium (reverse-engineering basics)
Points: 499

*End of README*
