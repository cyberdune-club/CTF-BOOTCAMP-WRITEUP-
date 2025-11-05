CC=gcc
CFLAGS=-O2 -fno-stack-protector -no-pie -z relro -z now
LDFLAGS=
BIN=hft

all: $(BIN)

$(BIN): main.c
	$(CC) main.c -o $(BIN) $(CFLAGS) $(LDFLAGS)

clean:
	rm -f $(BIN)