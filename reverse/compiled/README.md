# README.md — miaw_chal.py (Simple reversing challenge)

## Challenge summary

`miaw_chal.py` is a small Python challenge (distributed as a compiled/obfuscated Python binary) that verifies a single expected flag string by running a deterministic byte-wise transformation and comparing the result to a stored byte table.

* Expected flag format: `CYBERDUNE{MIAW_compiled}` (length 24 bytes)
* Goal: recover the input string that, after the challenge's `transform()` function, equals the `STORED` byte table.

## Provided code (behavioral outline)

The challenge performs the following steps on the UTF-8 bytes of the provided input string `s`:

For each byte `b` at index `i`:

1. `b = (b + i) & 0xFF`
2. `b ^= 0xA5`
3. `b = (b + (i * 7)) & 0xFF`
4. `b = rol8(b, (3 * i + 1) % 8)`  — a left rotation of the byte by `((3*i + 1) % 8)` bits.

The final array of bytes is compared to the `STORED` array.

## Approach to solve

To recover the original input, reverse the `transform()` — i.e., for each position `i` invert the operations in reverse order.

Operation reversal order (per-byte):

* Let `x` be the stored transformed byte (from `STORED[i]`).
* Step A (inverse of `rol8` left-rotate by `r`): perform a right-rotate by `r` bits.
* Step B (inverse of `b = (b + (i*7)) & 0xFF`): subtract `(i*7)` modulo 256.
* Step C (inverse of `b ^= 0xA5`): XOR with `0xA5` again (XOR is self-inverse).
* Step D (inverse of `b = (b + i) & 0xFF`): subtract `i` modulo 256.

After reversing, the resulting byte should be the original ASCII value of the flag at position `i`.

## Reversing script (Python)

Below is a ready-to-run solver that implements the inverse transform on the stored bytes and prints the recovered flag.

```python
# solver.py — reverse the transform and print the flag

STORED = [205, 96, 247, 8, 225, 15, 65, 72, 64, 6, 28, 248, 135, 28, 81, 16, 148, 37, 210, 121, 54, 114, 203, 180]

def ror8(v, r):
    r &= 7
    return ((v >> r) | ((v << (8 - r)) & 0xFF)) & 0xFF

def reverse_transform(stored):
    out_bytes = []
    for i, x in enumerate(stored):
        r = (3 * i + 1) % 8
        b = ror8(x, r)                       # inverse rotate
        b = (b - (i * 7)) & 0xFF            # inverse add i*7
        b = b ^ 0xA5                        # inverse xor
        b = (b - i) & 0xFF                  # inverse add i
        out_bytes.append(b)
    return bytes(out_bytes)

if __name__ == '__main__':
    flag_bytes = reverse_transform(STORED)
    try:
        flag = flag_bytes.decode('utf-8')
    except UnicodeDecodeError:
        flag = flag_bytes
    print('Recovered:', flag)
```

Run with `python3 solver.py` and it will print the recovered flag.

## Hints (for players)

* The transformation is purely byte-wise and reversible — no brute-force needed.
* XOR with a constant is its own inverse.
* Rotation by `r` bits is reversed by rotating the other direction by the same `r`.
* Pay attention to `& 0xFF` (operations are modulo 256).

## Solution

Running the reverse script recovers the flag:

```
CYBERDUNE{MIAW_compiled}
```

## Notes for authors

* The challenge is low-difficulty (easy) for players familiar with reversing deterministic byte transforms.
* To increase difficulty: randomize per-instance constants, mix in non-linear operations (S-boxes), or split the check across multiple files.
* Avoid using `len` mismatch messages that expose internals (optional: accept arbitrary padding and check only a prefix) if you want to increase realism.

---

*End of README*
