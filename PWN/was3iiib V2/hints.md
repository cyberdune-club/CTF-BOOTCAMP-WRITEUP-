# Hints

- gets() into a heap allocation: where can that lead without free()?
- Consider the top chunk and what happens if an allocation "doesn't fit."
- mmap-threshold hint: chunks may land near TLS.
- TLS holds a pointer to tcache_perthread_struct.
- With modern GLIBC, __free_hook and __malloc_hook are gone; setcontext(+32) can save you!
- Explore how to control heap state, and try leaking both heap and libc.
- You need to pivot from heap overflow to mmap chunk overflow for next phase.

# Instance
- Port: 31344
- Timeout: 180 seconds per instance
- Flag: in /flag.txt
- Format: CYBERDUNE{w_aaaaaaaa_S3I_bb00_BRAVO_3LIK_ILA_SOLVITIH_CH00}