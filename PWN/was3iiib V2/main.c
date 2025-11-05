#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>

enum { PKT_OPT_PING, PKT_OPT_ECHO, PKT_OPT_TRADE } typedef pkt_opt_t;
enum { PKT_MSG_INFO, PKT_MSG_DATA } typedef pkt_msg_t;

struct { size_t sz; uint64_t data[]; } typedef pkt_t;

const struct { char *header; char *color; } type_tbl[] = {
    [PKT_MSG_INFO] = {"PKT_INFO", "\x1b[1;34m"},
    [PKT_MSG_DATA] = {"PKT_DATA", "\x1b[1;33m"},
};

static void putl(pkt_msg_t type, const char *msg) {
    printf("%s%s\x1b[m:[%s]\n", type_tbl[type].color, type_tbl[type].header, msg);
    fflush(stdout);
}

static void alarm_handler(int sig) {
    (void)sig;
    _exit(0);
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    signal(SIGALRM, alarm_handler);
    alarm(180); // instance auto-shutdown in 180s

    putl(PKT_MSG_INFO, "BOOT_SQ");

    for (;;) {
        putl(PKT_MSG_INFO, "PKT_RES");

        size_t sz = 0;
        if (fread(&sz, sizeof(size_t), 1, stdin) != 1) {
            break;
        }

        pkt_t *pkt = malloc(sz);
        if (!pkt) { break; }
        pkt->sz = sz;

        // Vulnerability: unbounded gets on heap
        gets((char *)&pkt->data);

        switch (pkt->data[0]) {
        case PKT_OPT_PING:
            putl(PKT_MSG_DATA, "PONG_OK");
            break;
        case PKT_OPT_ECHO:
            putl(PKT_MSG_DATA, (char *)&pkt->data[1]);
            break;
        default:
            putl(PKT_MSG_INFO, "E_INVAL");
            break;
        }
    }

    putl(PKT_MSG_INFO, "BOOT_EQ");
    return 0;
}