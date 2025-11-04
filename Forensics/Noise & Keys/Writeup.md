# 🧠 Noise & Keys — Network + Crypto Forensics Challenge

---

## 📘 Description
A seemingly ordinary HTTP download hides a secret.  
Inside a captured `.pcapng`, there’s an encrypted flag waiting for decryption — but first, you’ll need to extract the right file from the noise.

Your mission: **recover and decrypt the hidden flag.**

---

## 🧰 Files Provided
- `challenge.pcapng` → network capture containing the transmitted ZIP file  
- (optional screenshots folder if you want to show Wireshark views)

---

## 🧠 Skills Tested
- Network forensics with `tshark` / `Wireshark`
- HTTP object extraction
- Zip file handling
- AES-CBC decryption using command-line tools
- Hex & Base16 conversions
- Bash scripting

---

## 💡 Steps / Hints

### 🥇 1. Extract files from the PCAP
Use `tshark` to export HTTP objects:
```bash
mkdir -p http_objs
tshark -r challenge.pcapng --export-objects "http,http_objs"
This should extract a ZIP file (e.g. challenge.zip) inside http_objs/.

🥈 2. Inspect and unzip
bash
Copier le code
file http_objs/challenge.zip
unzip http_objs/challenge.zip -d extracted_dir
cat extracted_dir/flag.txt
You’ll find something like:

makefile
Copier le code
AES-CBC
KEY_HEX: 7c251549826d9e4734b07e92acc752c
IV_HEX: 4151013bd4ab890b47922b0c0245538
CT_BASE16: aaca93e41b5903f6af6133bb111cf9766695cebae5ced72e64170e55be1c68948382f17008d83c32955f03bc482ed8
🥉 3. Extract values & decrypt using OpenSSL

le code
KEY=$(grep -i 'KEY_HEX' extracted_dir/flag.txt | cut -d: -f2 | tr -d ' \r\n')
IV=$(grep -i 'IV_HEX' extracted_dir/flag.txt | cut -d: -f2 | tr -d ' \r\n')
CT_HEX=$(grep -i 'CT_BASE16' extracted_dir/flag.txt | cut -d: -f2 | tr -d ' \r\n')

echo "$CT_HEX" | xxd -r -p > ct.bin
openssl enc -aes-128-cbc -d -in ct.bin -out flag_plain.txt -K "$KEY" -iv "$IV"
cat flag_plain.txt
🧩 Example Output
Copier le code
CYBERDUNE{encrypted_masterpiece_2025}


🔬 Full Walkthrough (Optional)
Step 1 — Extract the HTTP object
bash
Copier le code
tshark -r challenge.pcapng --export-objects "http,http_objs"
→ The extracted file is challenge.zip.

Step 2 — Inspect the ZIP
bash
Copier le code
unzip -l http_objs/challenge.zip
unzip http_objs/challenge.zip -d extracted_dir
cat extracted_dir/flag.txt
It contains AES parameters (key, IV, ciphertext).

Step 3 — Decrypt manually (Python alternative)
python
Copier le code
from Crypto.Cipher import AES

key = bytes.fromhex("7c251549826d9e4734b07e92acc752c")
iv = bytes.fromhex("4151013bd4ab890b47922b0c0245538")
ct = bytes.fromhex("aaca93e41b5903f6af6133bb111cf9766695cebae5ced72e64170e55be1c68948382f17008d83c32955f03bc482ed8")

cipher = AES.new(key, AES.MODE_CBC, iv)
flag = cipher.decrypt(ct)
print(flag.decode(errors='ignore'))
→ Output:

Copier le code
CYBERDUNE{encrypted_masterpiece_2025}
