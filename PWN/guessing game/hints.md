# Hints for Guessing Game PWN Challenge

## Hint 1 - Random Analysis 🎲
The rand() function is being used without srand(). What does this mean for the "randomness" of the generated numbers?

## Hint 2 - Vulnerability Location 🔍  
Look carefully at the win() function. Compare the buffer size with the amount of data being read.

## Hint 3 - Security Mitigations 🛡️
Check what security features are disabled in the Makefile. This will help you understand what exploitation techniques are possible.

## Hint 4 - Static Linking Advantage ⚙️
Static linking means all library functions are included in the binary. What does this give you for ROP chain construction?

## Hint 5 - Two-Stage Attack 🎯
You might need to exploit the vulnerability twice - once to set up your attack, and once to execute it.

## Hint 6 - Memory Layout 🗺️
Use tools like `vmmap` in GDB to find writable memory segments where you can store your payload.

## Hint 7 - Gadget Hunting 🔧
ROPgadget is your friend for finding useful gadgets in the static binary:
```bash
ROPgadget --binary vuln | grep "pop rdi"
```

## Hint 8 - Syscall Knowledge 📚
For x86_64 Linux:
- execve syscall number: 0x3b
- Arguments: rdi (filename), rsi (argv), rdx (envp)

## Final Hint 💡
The exploitation flow: Crack PRNG → Trigger overflow → Write "/bin/sh" → Return to main → Trigger overflow again → Execute syscall
