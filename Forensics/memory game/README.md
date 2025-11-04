# 🧩 Challenge — Memory Fragments (Forensics)

## 📘 Short description
You are provided with a raw memory dump delivered as text (`dump.txt`) which contains embedded base64 blobs and encrypted fragments.  
Your goal is to extract, decode and reassemble the hidden flag.

## 🧰 Files provided
- `dump.txt` — raw text received from network (contains base64, hex fragments, etc.)
- `dump.b64` — (optional) cleaned base64 extracted from `dump.txt`
- `dump.bin` — (optional) binary produced after base64 decode
- `xflag.png` / screenshots — analysis screenshots

## 🧠 Skills tested
- Text processing / regex
- Base64 decoding / binary handling
- Byte-wise XOR decryption
- Reassembling fragments by offset

## 💡 Hints (progressive)
1. Look for long base64-like blocks in `dump.txt`.  
   ```bash
   grep -Eo '([A-Za-z0-9+/]{80,}={0,2})' dump.txt | tr -d '\n' > dump.b64


   
base64 -d dump.b64 > dump.bin
file dump.bin
Inspect dump.bin for markers such as OFFSET_ and hex-encoded fragments:

bash
Copier le code
strings dump.bin | grep OFFSET
Fragments are hex strings annotated with offsets. Convert them back to bytes, then decrypt each fragment using a repeating XOR key.

Sort fragments by offset and stitch them together to produce the flag.

🔎 Quick commands
bash
Copier le code
# extract candidate base64, decode
grep -Eo '([A-Za-z0-9+/]{80,}={0,2})' dump.txt | tr -d '\n' > dump.b64
base64 -d dump.b64 > dump.bin

# search for offset-marked hex fragments
strings dump.bin | grep -Eo 'OFFSET_[0-9a-fA-F]+' -n

# or use the provided Python script: extract_flag.py
python3 extract_flag.py
#Final flag (SPOILER)

SPOILER: CYBERDUNE{m3m0ry_f0r3ns1cs_m4st3r_gH4d1_t5ebb3r}
