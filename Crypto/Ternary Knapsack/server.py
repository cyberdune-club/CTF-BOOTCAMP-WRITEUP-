# CYBERDUNE CTF - Ternary Knapsack Challenge Generator
# Generates output.txt with the exact same structure as the original

from Crypto.Util.number import *
from random import *

# Your specified flag
flag = b'CYBERDUNE{flag_for_testing}'

def int_to_ternary(n):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(n % 3)
        n = n // 3
    return digits[::-1]

# Process flag exactly like the original
flag = flag.strip(b"CYBERDUNE{").strip(b"}")
flag_int = bytes_to_long(flag)
flag_ternary = int_to_ternary(flag_int)

print(f"Original flag: CYBERDUNE{{flag_for_testing}}")
print(f"Flag content: {flag}")
print(f"Flag as integer: {flag_int}")
print(f"Flag ternary length: {len(flag_ternary)}")

# Same cryptographic setup as original
g = 2
length = len(flag_ternary)
p = getPrime(1024)
q = getPrime(1024)
n = p * q
bag = flag_ternary
A = [randint(1, n-1) for _ in range(length)]

print(f"Generated {length} variables for ternary knapsack")
print(f"p = {p}")
print(f"q = {q}")
print(f"n = p*q ({n.bit_length()} bits)")

# Compute s exactly like the original
s = 1
for i in range(length):
    s *= pow(g, (bag[i] * A[i]), n**2)
    s %= n**2

print(f"Computed s = {s}")

# Generate output.txt with exact same format
print("Generating output.txt...")

with open("output.txt", "w") as f:
    f.write(f"p = {p}\n")
    f.write(f"q = {q}\n")
    f.write(f"gA = {[pow(g, a, n**2) for a in A]}\n")
    f.write(f"s = {s}\n")

print("Successfully generated output.txt")
print("\nChallenge Summary:")
print("- Players receive: p, q, gA array, s")
print("- Goal: Find flag_ternary[i] ∈ {0,1,2} such that s = ∏(g^(flag_ternary[i] * A[i])) mod n²")
print("- Solution: CYBERDUNE{flag_for_testing}")
print("- Difficulty: Hard (requires Paillier decryption + ternary knapsack solving)")
