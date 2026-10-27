CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -lws2_32

# Bài 1
server: server.c
	$(CC) $(CFLAGS) -o server server.c $(LDFLAGS)

client: client.c
	$(CC) $(CFLAGS) -o client client.c $(LDFLAGS)

# Bài 2
server2: server2.c
	$(CC) $(CFLAGS) -o server2 server2.c $(LDFLAGS)

client2: client2.c
	$(CC) $(CFLAGS) -o client2 client2.c $(LDFLAGS)

# Clean
clean:
	del /Q server client server2 client2 server.exe client.exe server2.exe client2.exe

# All
all: server client server2 client2

.PHONY: clean all
