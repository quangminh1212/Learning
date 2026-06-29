CC = gcc
CFLAGS = -Wall -Wextra -O2

# Linux
LDFLAGS_LINUX = -lresolv
# Windows
LDFLAGS_WINDOWS = -lws2_32

# Detect OS
UNAME_S := $(shell uname -s)
ifeq ($(OS),Windows_NT)
    LDFLAGS = $(LDFLAGS_WINDOWS)
    RM = del /Q
else
    LDFLAGS = $(LDFLAGS_LINUX)
    RM = rm -f
endif

# Target cho bài 1
resolver: resolver.c
	$(CC) $(CFLAGS) -o resolver resolver.c $(LDFLAGS)

# Target cho bài 2
resolver2: resolver2.c
	$(CC) $(CFLAGS) -o resolver2 resolver2.c $(LDFLAGS)

# Clean
clean:
	$(RM) resolver resolver2 resolver.log resolver.exe resolver2.exe

# All
all: resolver resolver2

.PHONY: clean all
