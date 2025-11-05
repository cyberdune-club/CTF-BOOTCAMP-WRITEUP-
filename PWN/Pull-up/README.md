# CYBERDUNE - Push Pull Pops

**Category:** pwn / remote  
**Port:** 31341  
**Instance lifetime:** 180 seconds (3 minutes)  
**Format:** Flag is inside `app/flag.txt` and follows `CYBERDUNE{...}`

## Overview
This challenge emulates the "Push pull pops" vuln: the server accepts **base64**-encoded bytes, disassembles them with **Capstone**, and only allows the instructions `push`, `pop`, and `int3` (with the first operand of `push`/`pop` required to be a register). If the check fails, the server rejects the input.

There is a disassembler bug/edge-case: some machine-code sequences are **valid to the CPU**, but Capstone fails to decode them correctly, causing the `check()` function to consider them invalid and stop disassembling early. If you place such an instruction as the **first instruction** in your payload, the check will abort and will not validate the following bytes — letting your real shellcode pass.

## Goal
- Exploit this behavior to run shellcode on the server and read `app/flag.txt`.
- The server will automatically stop after 180 seconds.

## Hints
1. There is a specific two-byte instruction that Capstone mis-handles — it is valid and executes correctly on x86_64 CPUs.
2. The working exploit for the original challenge used the bytes: `\x63\xc8` (which correspond to `movsxd ecx, eax` when assembled a certain way).
3. Prepend that 2-byte sequence to your normal shellcode, base64-encode, and send it to the service.
4. The server duplicates the accepted socket to `stdin/out/err` before executing the code, so an interactive shell spawned by your shellcode will be attached to the network socket.

## Provided files
- `app.py` — the vulnerable service (uses Capstone). Binds 0.0.0.0:31341. Auto-exits after 180s.
- `Dockerfile` — minimal image to run the service.
- `app/flag.txt` — the flag.
- `solve.py` — example exploit that crafts a payload and connects to the service.
