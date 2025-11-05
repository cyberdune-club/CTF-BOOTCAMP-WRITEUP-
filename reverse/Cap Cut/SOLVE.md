# SOLVE.md — fake_app.apk (CapCut Pro CTF)

**Challenge summary**

A supplied APK (`fake_app.apk`) contained an `assets/strings.txt` file which looked like it held useful strings and encoded data. The goal was to extract and decode the asset to recover the flag.

---

## Findings (short)

* The flag was found inside `assets/strings.txt` as a Base64-encoded string.
* Decoded flag: `CYBERDUNE{Fr3ak1ng_APK_R3v3rs3}`

---

## Environment & tools

Typical tooling used for APK static analysis and simple extraction:

* Linux (or WSL / macOS)
* `unzip`, `strings`, `grep`, `base64`
* `apktool` (optional) — for resources and manifest
* `jadx` / `jadx-gui` or `jadx` CLI — for decompiling `classes.dex` to Java
* `baksmali` / `smali` (optional)
* `xxd`, `hexdump` (optional)

All commands below were executed locally from a shell.

---

## Files observed inside the APK (relevant excerpt)

```
AndroidManifest.xml
classes.dex
assets/strings.txt
assets/readme.txt
```

---

## Step-by-step reproduction

1. **List archive contents**

```bash
unzip -l fake_app.apk
```

Look for `assets/strings.txt` in the listing.

2. **Extract the asset file**

```bash
unzip fake_app.apk assets/strings.txt -d extracted/
# resulting file -> extracted/assets/strings.txt
```

Or with `7z`:

```bash
7z e fake_app.apk assets/strings.txt -oextracted/
```

3. **Inspect the file**

```bash
cat extracted/assets/strings.txt
```

Example contents from the challenge (observed):

```
welcome_to_capcut_pro_ctf
version: 9.9.9-mod
// decoy keys:
KEY_API=3ab7f1c9
// suspicious_string (maybe base64?):
Q1lCRVJEVU5Fe0ZyM2FrMW5nX0FQS19SM3YzcnMzfQ==
// random noise:
ZmFrZV9kYXRhXzEyMw==
```

4. **Decode the Base64 lines**

You can decode the suspicious lines with `base64 --decode` (or `python -m base64`):

```bash
# decode the flag-looking string
echo 'Q1lCRVJEVU5Fe0ZyM2FrMW5nX0FQS19SM3YzcnMzfQ==' | base64 --decode
# output -> CYBERDUNE{Fr3ak1ng_APK_R3v3rs3}

# decode the noise string
echo 'ZmFrZV9kYXRhXzEyMw==' | base64 --decode
# output -> fake_data_123
```

5. **Optional — search for in-app usage**

If you need to know whether the flag or KEY_API is referenced anywhere in the code or used to gate behavior, decompile `classes.dex` and search for references:

```bash
# Convert APK -> decompiled Java using jadx (CLI)
jadx -d jadx_out fake_app.apk
# Search for the asset filename or key usage
grep -R "assets/strings.txt" -n jadx_out || true
grep -R "KEY_API" -n jadx_out || true
```

Also with `apktool` you can inspect smali and resources:

```bash
apktool d fake_app.apk -o apktool_out
grep -R "strings.txt" -n apktool_out || true
```

6. **Capture the flag**

From step 4 the decoded flag is:

```
CYBERDUNE{Fr3ak1ng_APK_R3v3rs3}
```

Record it as the solution for the challenge.

---

## Notes & analysis

* The challenge used a very common and low-effort protection/obfuscation: storing sensitive data in `assets/` encoded in Base64. Base64 is reversible and not encryption.
* `KEY_API=3ab7f1c9` looks like a decoy. Always search the code for usages; sometimes decoys are used to hide the real secret.
* `assets/` files are bundled in plain view inside APKs (ZIP). Treat APKs like ZIP archives for extraction and quick inspection.

---

## Recommendations / Hardening (if this were a real app)

1. Never store secrets (flags, API keys, tokens, secrets) in the APK where they can be trivially extracted. If required, keep secrets server-side and authenticate requests.
2. If embedding sensitive data is unavoidable (it almost never is), use strong cryptography with keys not embedded in the same binary.
3. Use runtime checks and server-side gating so that the client cannot reveal secrets by static analysis.
4. Obfuscation (ProGuard, R8) may slow an attacker but won't stop a determined reverse engineer.

---

## Artifacts

* `extracted/assets/strings.txt` — recovered file
* `jadx_out/` — optional decompiled Java for deeper analysis
* `apktool_out/` — optional smali/resources

---

## TL;DR

Open the APK as a ZIP, extract `assets/strings.txt`, decode the Base64 string and you get the flag: `CYBERDUNE{Fr3ak1ng_APK_R3v3rs3}`.

---

*End of write-up.*
