CC=gcc
CFLAGS=-no-pie -fno-stack-protector -static

vuln: vuln.c
	$(CC) $(CFLAGS) -o vuln vuln.c

clean:
	rm -f vuln

.PHONY: clean