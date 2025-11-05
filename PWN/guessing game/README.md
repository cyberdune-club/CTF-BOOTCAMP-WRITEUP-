# Guessing Game PWN Challenge

## Description
Welcome to the Guessing Game! Can you beat our "random" number generator and find a way to win more than just a congratulatory message?

**Category:** Binary Exploitation  
**Difficulty:** Medium  
**Points:** 350  
**Flag Format:** CYBERDUNE{...}

## Challenge Details
You're given a simple guessing game that asks you to predict a "randomly" generated number. But there's more to this game than meets the eye...

The binary is statically linked and has some interesting security features (or lack thereof). Your goal is to find a way to get a shell on the remote server and capture the flag.

## Files Provided
- `vuln` - The challenge binary
- `vuln.c` - Source code (for analysis)
- `Makefile` - Build configuration

## Remote Instance
- **Host:** [TO_BE_CONFIGURED]
- **Port:** [TO_BE_CONFIGURED] 
- **Timeout:** 180 seconds

## Learning Objectives
- Understanding predictable PRNG vulnerabilities
- Buffer overflow exploitation techniques
- ROP (Return Oriented Programming) chains
- Static binary analysis
- Multi-stage exploitation

## Initial Analysis Questions
1. What makes the random number generator predictable?
2. Where is the buffer overflow vulnerability located?
3. What security mitigations are enabled/disabled?
4. How can you leverage the static linking for exploitation?

Good luck, and may the ROP be with you! 🎯
