# Guessing Game PWN Challenge - Complete Writeup

## Challenge Overview
This is a classic buffer overflow challenge combined with a predictable PRNG vulnerability. The challenge requires a two-stage ROP chain exploitation.

## Initial Analysis

### Binary Information
```bash
file vuln
# vuln: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, not stripped

checksec vuln
# RELRO: Partial RELRO
# Stack: No canary found  
# NX: NX enabled
# PIE: No PIE
```

### Key Observations
1. **Static linking** - Provides many ROP gadgets
2. **No stack canary** - Buffer overflow is straightforward
3. **NX enabled** - No shellcode injection
4. **No PIE** - Fixed addresses, no ASLR bypass needed

## Vulnerability Analysis

### 1. Predictable PRNG
```c
long get_random() {
    return rand() % BUFSIZE;  // No srand() seed!
}
```
The rand() function uses a default seed, making the sequence predictable.

### 2. Buffer Overflow in win()
```c
void win() {
    char winner[BUFSIZE];           // 100 bytes buffer
    printf("New winner!\nName? ");
    fgets(winner, 360, stdin);      // Reads up to 360 bytes!
    printf("Congrats %s\n\n", winner);
}
```

## Exploitation Strategy

### Phase 1: Crack the Random Sequence
Since rand() uses a default seed, we can brute force the sequence:

```python
def crack_sequence():
    sequence = []
    for i in range(10):  # Get first 10 numbers
        for guess in range(1, 101):
            # Try each number until we get "Congrats!"
            # Build sequence incrementally
```

**Found sequence:** [84, 87, 78, 16, 94, ...]

### Phase 2: Two-Stage ROP Exploitation

#### Stage 1: Write "/bin/sh" to memory
1. Use buffer overflow to control RIP
2. ROP chain to call read(0, bss_addr, 8) 
3. Write "/bin/sh\x00" to BSS segment
4. Return to main() to trigger vulnerability again

#### Stage 2: Execute syscall
1. Second buffer overflow
2. ROP chain for execve("/bin/sh", 0, 0)
3. Get shell access

## ROP Gadgets Required

```bash
ROPgadget --binary vuln | grep -E "(pop rdi|pop rsi|pop rdx|pop rax|syscall)"
```

Essential gadgets:
- `pop rdi; ret` - First argument  
- `pop rsi; ret` - Second argument
- `pop rdx; ret` - Third argument  
- `pop rax; ret` - Syscall number
- `syscall; ret` - Execute syscall

## Memory Layout

Find writable memory with GDB:
```bash
gdb ./vuln
(gdb) start
(gdb) vmmap
# Look for BSS section (writable)
```

## Complete Exploit Code

The solve.py script implements:
1. Random sequence cracking
2. Two-stage ROP chain
3. Remote/local exploitation modes

### Key exploit steps:
```python
# Stage 1 payload
payload1 = padding + rop_chain_read + return_to_main
# Stage 2 payload  
payload2 = padding + rop_chain_execve
```

## Flag Capture

After successful exploitation:
```bash
$ cat flag.txt
CYBERDUNE{9c547ebf0ea97fd40cf30217f2f67427ad347675cbf77cc59e29efb7852fa8a2}
```

## Mitigation Recommendations

1. **Use secure PRNG** - Seed with time/entropy
2. **Bounds checking** - Use strncpy, check buffer sizes
3. **Stack canaries** - Enable stack protection
4. **ASLR/PIE** - Enable address randomization
5. **FORTIFY_SOURCE** - Enable compile-time protections

## Learning Outcomes

- Understanding predictable randomness vulnerabilities
- Multi-stage ROP chain construction
- Static binary exploitation techniques
- Importance of proper input validation

---

**Author:** CYBERDUNE CTF Team  
**Difficulty:** Medium  
**Category:** Binary Exploitation
