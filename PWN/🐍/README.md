CYBERDUNE - 🐍
==================

Name: CYBERDUNE (heap0)
Author: marlithor_cyber

Description:
------------
A small heap-based overflow challenge. The binary allocates two small heap
chunks: `input_data` and `safe_var`. `input_data` is read with an unsafe
scanf("%s", input_data) so a long write can overflow and overwrite data in
the heap, potentially modifying `safe_var`. If `safe_var` is different from
"bico", the program prints the flag.

Modifications in this distribution:
- All occurrences of "pico" replaced with "CYBERDUNE" labeling.
- FLAGSIZE_MAX increased to 128 to support a longer flag.
- The program will auto-terminate after 180 seconds (3 minutes) using alarm().
- Provided a placeholder `flag.txt` containing a dummy flag.
- Included a brute-force exploit script `solve.py` that tries varying payload
  lengths to overwrite `safe_var` and triggers the flag-print path.

Build:
------
Recommended gcc command to build the binary locally:

    gcc -g -O0 chall.c -o heap0 -fno-stack-protector -z execstack -no-pie

Or using the Makefile included:

    make

Run locally:
------------
./heap0

Run against remote instance:
----------------------------
Host: 159.223.23.56
Port: 31340

The supplied exploit `solve.py` defaults to this host/port. Example:

    python3 solve.py --host 159.223.23.56 --port 31340

Files included:
- chall.c         (modified source)
- flag.txt        (placeholder)
- solve.py        (exploit script)
- Makefile        (build command)
- README.txt
