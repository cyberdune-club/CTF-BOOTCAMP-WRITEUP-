# CYBERDUNE Challenge - mmaped memory manufactures meticulous menaces

## Build Instructions
```bash
docker build -t cyberdune_hft .
docker run --rm -p 31344:31344 cyberdune_hft
```

## Files to distribute to players:
- hft (compiled binary)
- main.c
- description.md
- hints.md

## Testing
```bash
# Connect locally
nc 127.0.0.1 31344

# Run solve script
python3 solve.py
```

## Challenge Summary
- Heap exploitation via gets() overflow
- No free() calls available
- Top chunk manipulation for leaks
- mmap chunks near TLS
- Target: RCE via modern techniques (setcontext+32)
- Auto-timeout: 180 seconds