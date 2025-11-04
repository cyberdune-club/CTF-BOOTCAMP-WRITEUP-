investigation_encoded_2
=======================
A small CTF forensic/encoding challenge.

Files:
- mystery.enc : the encoded blob (single-line text)
- clue.txt    : a short hint
- solve.py    : a solver script (python3)
- writeup.md  : a writeup explaining how it was solved
- README.md   : this file

Objective: Recover the flag in the format CYBERDUNE{...}

Hints:
- Try reversing the data.
- Layers include hex, base64, and compression.
