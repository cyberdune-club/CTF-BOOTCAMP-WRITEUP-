🕵️‍♂️ Challenge Description

A digital officer’s USB drive was seized during an investigation.
Hidden somewhere inside the disk.img is confidential information.

Your job: extract the truth from the image.

🔍 Step 1 — Quick Inspection
The simplest first step in any forensic challenge is to check for human-readable strings:

strings disk.img | less
Scrolling through the output, something suspicious immediately appears:

flag.txtCYBERDUNE{c4rv1ng_th3_truth}

The PK signature (0x50 0x4B) indicates a ZIP structure — but here, it’s part of the flag text.

The flag itself is clearly embedded in plain text inside the image.

✅ Final Flag

CYBERDUNE{c4rv1ng_th3_truth}
