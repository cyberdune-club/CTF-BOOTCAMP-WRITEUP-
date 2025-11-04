# 🧩 Challenge — JS Layers (Forensics)

## 📘 Description
You are given a JPEG file named `Nass_kay3raw_JS_ana_ach_kandir_haha.jpg`.  
At first glance, the image looks harmless — but something is clearly hidden inside.  
A simple metadata check (`binwalk`, `strings`) reveals a suspicious Base64 string.  
Your task: peel back the layers and uncover the real flag!

---

## 🧠 Skills Tested
- File analysis (JPEG inspection)
- Multi-layer Base64 decoding
- Using Python for quick decoding
- Basic digital forensics

---

## 🧰 Provided Files
- `Nass_kay3raw_JS_ana_ach_kandir_haha.jpg` — suspicious image  
- `XFLAG.png` — screenshot of the analysis steps and final decoded flag

---

## 💡 Hint
When you find a long random-looking string (like `VVRG...`), try decoding it — maybe several times 😉  
You can use either online Base64 decoders or a quick Python one-liner.

Example:
```bash
python3 -c "import base64; s='YOUR_STRING'; print(base64.b64decode(s))"


tep-by-step solution summary

Run a file check:

Search for readable strings:

strings Nass_kay3raw_JS_ana_ach_kandir_haha.jpg


→ Found: VVRG1ExSUdTa1ZXV...RbFLNRDA9

Decode multiple Base64 layers using Python:

python3 -c "import base64; s='VVRG1ExSUdTa1ZXV...RbFLNRDA9'; print(base64.b64decode(base64.b64decode(base64.b64decode(s))).decode())"


The final decoded string reveals the flag:

CYBERDUNE{B1n4vLk_C4n_S33_Th1s!}
