CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -lresolv

# Target cho bài 1
resolver: resolver.c
	$(CC) $(CFLAGS) -o resolver resolver.c $(LDFLAGS)

# Target cho bài 2
resolver2: resolver2.c
	$(CC) $(CFLAGS) -o resolver2 resolver2.c $(LDFLAGS)

# Clean
clean:
	rm -f resolver resolver2 resolver.log

# All
all: resolver resolver2

.PHONY: clean all
