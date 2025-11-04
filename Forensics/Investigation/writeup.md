# Writeup — investigation_encoded_2 (CYBERDUNE)

**Challenge description (summary)**  
You are given a file `mystery.enc` and a small textual hint. The goal is to recover the flag in the format `CYBERDUNE{...}`.

**What I found**  
- `mystery.enc` contains a long single-line string of hex characters that looks scrambled.
- The clue mentioned reversing and common layers (hex, base64, compression).

**Manual solving steps**  
1. Reverse the string (the challenge author reversed the hex to add a layer).  
   Example (bash): `rev mystery.enc > step1.txt`  
2. Convert hex back to raw bytes:  
   `xxd -r -p step1.txt > step2.bin`  
3. Base64-decode the result:  
   `base64 -d step2.bin > step3.bin`  
4. Decompress using zlib (python works well):  
   ```python
   import zlib
   comp = open('step3.bin','rb').read()
   print(zlib.decompress(comp).decode())
   ```
5. The output is the flag: `CYBERDUNE{...}`

**Automated solve**  
There's a `solve.py` included that performs the exact reversing steps:
```
python3 solve.py mystery.enc
```

**Flag (kept out of the writeup here to preserve challenge integrity)**  
_The solver prints the full flag._

-- End of writeup.
