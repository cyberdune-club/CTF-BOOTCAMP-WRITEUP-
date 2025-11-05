CC = gcc
CFLAGS = -g -O0 -fno-stack-protector -z execstack -no-pie
TARGET = heap0

all: $(TARGET)

$(TARGET): chall.c
	$(CC) $(CFLAGS) chall.c -o $(TARGET)

clean:
	rm -f $(TARGET)
