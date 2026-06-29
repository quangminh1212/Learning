CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -lws2_32

# Target cho bài 1
resolver: resolver.c
	$(CC) $(CFLAGS) -o resolver resolver.c $(LDFLAGS)

# Target cho bài 2
resolver2: resolver2.c
	$(CC) $(CFLAGS) -o resolver2 resolver2.c $(LDFLAGS)

# Clean
clean:
	del /Q resolver resolver2 resolver.log resolver.exe resolver2.exe

# All
all: resolver resolver2

.PHONY: clean all
