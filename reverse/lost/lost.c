// lost_chal.c
// Simple reversing challenge — input must match hidden flag.
// Compile: gcc -o lost_chal lost_chal.c

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

static unsigned char stored[] = {
    25,14,176,57,130,198,202,64,158,116,146,212,43,165,153,240,
    217,251,24,181,35,209,151,131,117,29,153,179,216,167,99,252
};
static const int STORED_LEN = sizeof(stored)/sizeof(stored[0]);

// small rotate-left (8-bit)
static unsigned char rol(unsigned char v, int r) {
    r &= 7;
    return (unsigned char)(((v << r) | (v >> (8 - r))) & 0xFF);
}

// decoy function to add noise for static analysis
void decoy_worker(const char *s){
    volatile int x = 0;
    for(int i=0;i< (int)strlen(s); ++i) x ^= (s[i] + i);
    if(x == 0xdeadbeef) puts("secret");
}

int main(void){
    char input[256];
    printf("Enter flag: ");
    if(!fgets(input, sizeof(input), stdin)) return 0;
    // strip newline
    size_t ln = strlen(input);
    if(ln && input[ln-1] == '\n') { input[ln-1] = 0; ln--; }

    decoy_worker(input); // noise

    if((int)ln != STORED_LEN){
        printf("Wrong length (expected %d)\n", STORED_LEN);
        return 0;
    }

    // perform the same transform as used to build stored[]
    for(int i=0;i<STORED_LEN;i++){
        unsigned char b = (unsigned char)input[i];
        b = (unsigned char)((b + (i & 0xFF)) & 0xFF);
        b = (unsigned char)(b ^ 0x5A);
        b = (unsigned char)((b + ((i*7)%256)) & 0xFF);
        b = rol(b, i % 7);
        if(b != stored[i]){
            printf("Nope.\n");
            return 0;
        }
    }

    puts("Correct! Flag accepted.");
    // in a real CTF you'd print the flag or give a shell; keep it simple here:
    return 0;
}
