#!/usr/bin/env python3
"""
CYBERDUNE Forensics Challenge Generator
Generates a realistic 800MB forensics challenge file
"""

import os
import random
import base64
import hashlib
from datetime import datetime

def xor_encrypt(data, key=0x42):
    """XOR encryption with key"""
    return bytes([b ^ key for b in data])

def generate_hex_dump(size_kb=50):
    """Generate realistic hex dump data"""
    lines = []
    for i in range(size_kb * 16):  # 16 lines per KB roughly
        offset = i * 16
        hex_data = ' '.join(f'{random.randint(0, 255):02x}' for _ in range(16))
        ascii_data = ''.join(chr(random.randint(32, 126)) if random.random() > 0.7 else '.' for _ in range(16))
        lines.append(f'{offset:08x}:  {hex_data}  |{ascii_data}|')
    return '\n'.join(lines)

def generate_network_packets(count=5000):
    """Generate fake network packet captures"""
    packets = []
    protocols = ['TCP', 'UDP', 'ICMP', 'DNS', 'HTTP', 'TLS']
    
    for i in range(count):
        src_ip = f'192.168.{random.randint(0,255)}.{random.randint(1,254)}'
        dst_ip = f'10.0.{random.randint(0,255)}.{random.randint(1,254)}'
        proto = random.choice(protocols)
        port = random.randint(1024, 65535)
        
        packet = f'[{i:06d}] {src_ip}:{port} -> {dst_ip} | {proto} | {random.randint(64, 1500)} bytes'
        packets.append(packet)
        
        # Hidden DNS clue
        if i == 3333:
            packets.append(f'[DNS_QUERY] flag-hint.cyberdune.local -> TXT "check_memory_offset_0x1E8480"')
    
    return '\n'.join(packets)

def generate_file_system_entries():
    """Generate fake file system structure"""
    files = [
        ('/root/secrets.txt.enc', 2048, '600', 'Encrypted with AES-256'),
        ('/home/user/Documents/passwords.kdbx', 8192, '600', 'KeePass Database'),
        ('/var/log/auth.log', 524288, '644', 'Authentication logs'),
        ('/var/log/syslog', 1048576, '644', 'System logs'),
        ('/etc/shadow.bak', 4096, '000', 'Shadow file backup'),
        ('/tmp/.hidden_flag.enc', 256, '600', 'Suspicious encrypted file'),
        ('/home/user/.bash_history', 16384, '600', 'Command history'),
        ('/opt/malware_sample.bin', 32768, '755', 'Potential malware'),
    ]
    
    entries = ['=' * 80, 'FILE SYSTEM ANALYSIS', '=' * 80, '']
    for path, size, perm, desc in files:
        entries.append(f'Path: {path}')
        entries.append(f'  Size: {size} bytes')
        entries.append(f'  Permissions: {perm}')
        entries.append(f'  Inode: {random.randint(100000, 999999)}')
        entries.append(f'  Description: {desc}')
        entries.append(f'  MD5: {hashlib.md5(path.encode()).hexdigest()}')
        entries.append('')
    
    return '\n'.join(entries)

def hide_flag_in_data(flag, method='xor_base64'):
    """Hide flag using multiple encoding layers"""
    if method == 'xor_base64':
        # XOR then Base64
        xored = xor_encrypt(flag.encode(), 0x42)
        encoded = base64.b64encode(xored).decode()
        return f'/* MEMORY_DUMP_0x1E8480: {encoded} */'
    elif method == 'reverse_hex':
        # Reverse and convert to hex
        reversed_flag = flag[::-1]
        hex_flag = reversed_flag.encode().hex()
        return f'REGISTRY_KEY_0xDEADBEEF: {hex_flag}'
    elif method == 'rot13_base64':
        # ROT13 + Base64
        rot13 = ''.join(chr((ord(c) - 97 + 13) % 26 + 97) if c.islower() else 
                        chr((ord(c) - 65 + 13) % 26 + 65) if c.isupper() else c 
                        for c in flag)
        return base64.b64encode(rot13.encode()).decode()
    
def generate_forensics_file(filename='evidence_disk_image.forensics', size_mb=800):
    """Generate the main forensics challenge file"""
    
    print(f'[+] Generating {size_mb}MB forensics challenge file...')
    print(f'[+] Output: {filename}')
    
    # The actual flag
    FLAG = 'CYBERDUNE{d33p_1n_th3_m3m0ry_dump_y0u_f0und_m3_h4ck3r}'
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Header
        f.write('=' * 80 + '\n')
        f.write('FORENSICS DISK IMAGE v2.1\n')
        f.write('=' * 80 + '\n')
        f.write(f'Acquisition Date: {datetime.now().isoformat()}\n')
        f.write(f'Evidence ID: CYBER-DUNE-2025-{random.randint(1000, 9999)}\n')
        f.write(f'Case Number: MA-SEC-{random.randint(10000, 99999)}\n')
        f.write(f'Image Size: {size_mb} MB\n')
        f.write(f'Hash Algorithm: SHA-256\n')
        f.write(f'Image Hash: {hashlib.sha256(FLAG.encode()).hexdigest()}\n')
        f.write('=' * 80 + '\n\n')
        
        # Hint section
        f.write('[INVESTIGATOR NOTES]\n')
        f.write('- Multiple encryption layers detected\n')
        f.write('- Possible XOR cipher usage (key unknown)\n')
        f.write('- Check memory offsets carefully\n')
        f.write('- DNS queries contain metadata\n')
        f.write('- Steganography suspected in image metadata\n\n')
        
        # Layer 1: Memory dump with hidden flag
        f.write('\n' + '=' * 80 + '\n')
        f.write('MEMORY DUMP - LAYER 1\n')
        f.write('=' * 80 + '\n\n')
        
        # Generate lots of hex dump data
        total_written = 0
        chunk_size = 100  # KB per chunk
        
        for chunk in range(size_mb * 10):  # Adjust multiplier for size
            # Write hex dump
            hex_data = generate_hex_dump(chunk_size)
            f.write(hex_data + '\n')
            
            # Hide flag at specific offset (2MB mark)
            if chunk == 20:
                f.write('\n' + '!' * 80 + '\n')
                f.write(f'{hide_flag_in_data(FLAG, "xor_base64")}\n')
                f.write('!' * 80 + '\n\n')
                print(f'[+] Flag hidden at chunk {chunk}')
            
            # Add fake encrypted blocks
            if chunk % 50 == 0:
                f.write(f'\n[ENCRYPTED_BLOCK_{chunk}]\n')
                f.write('AES-256-CBC:\n')
                f.write(base64.b64encode(os.urandom(128)).decode() + '\n')
                f.write('IV: ' + os.urandom(16).hex() + '\n\n')
            
            total_written += chunk_size
            if total_written % 10000 == 0:
                print(f'[+] Written {total_written // 1000} MB...')
        
        # Layer 2: Network captures
        f.write('\n\n' + '=' * 80 + '\n')
        f.write('NETWORK PACKET CAPTURE - LAYER 2\n')
        f.write('=' * 80 + '\n\n')
        f.write(generate_network_packets(8000) + '\n\n')
        
        # Layer 3: File system
        f.write('\n' + '=' * 80 + '\n')
        f.write('FILE SYSTEM ANALYSIS - LAYER 3\n')
        f.write('=' * 80 + '\n\n')
        f.write(generate_file_system_entries() + '\n\n')
        
        # Layer 4: Additional obfuscation
        f.write('\n' + '=' * 80 + '\n')
        f.write('ALTERNATE DATA STREAMS\n')
        f.write('=' * 80 + '\n\n')
        f.write(f'Stream_0x01: {hide_flag_in_data(FLAG, "reverse_hex")}\n')
        f.write(f'Stream_0x02: {hide_flag_in_data(FLAG, "rot13_base64")}\n\n')
        
        # Hints at the end
        f.write('\n' + '=' * 80 + '\n')
        f.write('FORENSIC EXAMINER NOTES\n')
        f.write('=' * 80 + '\n')
        f.write('Hint 1: XOR key might be 0x42 (ASCII: B)\n')
        f.write('Hint 2: Check memory offset 0x1E8480 (decimal: 2000000)\n')
        f.write('Hint 3: Flag format is CYBERDUNE{...}\n')
        f.write('Hint 4: Base64 encoding detected in memory dumps\n')
        f.write('Hint 5: Look for patterns between /* and */\n')
        f.write('=' * 80 + '\n')
    
    file_size = os.path.getsize(filename)
    print(f'\n[✓] File generated successfully!')
    print(f'[✓] Actual size: {file_size / (1024*1024):.2f} MB')
    print(f'[✓] Flag: {FLAG}')
    print(f'\n[!] Challenge ready! Good luck!\n')

def generate_solution_script():
    """Generate a solution script for reference"""
    solution = """#!/usr/bin/env python3
# Solution script for CYBERDUNE Forensics Challenge

import base64
import re

def xor_decrypt(data, key=0x42):
    return bytes([b ^ key for b in data])

def solve():
    # Read the forensics file
    with open('evidence_disk_image.forensics', 'r') as f:
        content = f.read()
    
    # Method 1: Find XOR+Base64 encoded flag
    pattern = r'/\* MEMORY_DUMP_0x[0-9A-F]+: ([A-Za-z0-9+/=]+) \*/'
    matches = re.findall(pattern, content)
    
    for match in matches:
        try:
            # Decode base64
            decoded = base64.b64decode(match)
            # XOR decrypt with key 0x42
            decrypted = xor_decrypt(decoded, 0x42)
            text = decrypted.decode('utf-8')
            if 'CYBERDUNE{' in text:
                print(f'[+] FLAG FOUND: {text}')
                return text
        except:
            pass
    
    return None

if __name__ == '__main__':
    solve()
"""
    
    with open('solve_challenge.py', 'w') as f:
        f.write(solution)
    print('[+] Solution script saved as: solve_challenge.py')

if __name__ == '__main__':
    print('\n🔥 CYBERDUNE FORENSICS CHALLENGE GENERATOR 🔥\n')
    
    # Generate the challenge file
    generate_forensics_file('evidence_disk_image.forensics', size_mb=800)
    
    # Generate solution script
    generate_solution_script()
    
    print('\n[+] Files created:')
    print('    - evidence_disk_image.forensics (challenge file)')
    print('    - solve_challenge.py (solution script)')
    print('\n[+] To solve: python3 solve_challenge.py\n')
