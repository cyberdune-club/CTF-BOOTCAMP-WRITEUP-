# mmaped memory manufactures meticulous menaces

## Story
A hyperactive HFT (high-frequency trading) engine streams packets over a custom protocol. It never frees, but trusts input blindly. Can you turn frequency into fragility?

## Files Provided
- Binary: hft
- Source: main.c

## Target
- Remote host listens on TCP port 31344
- Instance lifetime: 180 seconds

## Protocol
- Server prints "PKT_RES" before each request
- Client sends 8-byte little-endian size (size_t) 
- Server allocates malloc(sz), writes pkt->sz, then reads payload via gets(&pkt->data)
- The first qword of pkt->data is the option
  - 0 = PING => PKT_DATA:[PONG_OK]
  - 1 = ECHO => PKT_DATA:[echoed string at &pkt->data[1]]
  - otherwise => PKT_INFO:[E_INVAL]

## Goal
Get a shell and read /flag.txt

## Flag format
CYBERDUNE{w_aaaaaaaa_S3I_bb00_BRAVO_3LIK_ILA_SOLVITIH_CH00}

## Difficulty & Audience
Intermediate heap exploitation, inspired by "high frequency troubles"