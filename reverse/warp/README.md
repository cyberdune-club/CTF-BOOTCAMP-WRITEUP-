warp  — REVERSE CHALLENGE 

Rules
-----
- Binary: `obelisque` (Linux x86_64)
- Your goal: recover the exact flag.
- The flag format is `CYBERDUNE{...}`.

What you know
-------------
- The binary reads one line from stdin and either prints `OK!` + your input (if correct) or `nope.`
- It has anti-debug checks and non-trivial mix of transformations on the input.
- No networking, no file I/O beyond stdin/stdout.

How to run
----------
```
./obelisque
Enter flag: CYBERDUNE{your_guess_here}
```

Tips
----
- Static + dynamic analysis both matter.
- Look for any obfuscated constants and how they're combined at the end.
- There is a final 64-bit equality check after a lot of mixing.
- Opaque predicates and anti-debug are mild; bypass is possible.
