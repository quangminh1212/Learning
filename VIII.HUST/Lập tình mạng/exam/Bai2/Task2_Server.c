/*
 * Task2_Server.c - Server ma hoa/giai ma Caesar (da luong) - POSIX/Linux
 * Cu phap: server -p <PortNumber>
 * Nhan yeu cau (encrypt/decrypt + key) -> nhan file -> ma hoa/giai ma -> gui ket qua ve client
 * Compile tren Ubuntu: gcc -o server Task2_Server.c -pthread
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>

#define BUFFER_SIZE 8192   /* Kich thuoc buffer xu ly file */
#define OPCODE_ENCRYPT 0   /* Opcode: yeu cau ma hoa */
#define OPCODE_DECRYPT 1   /* Opcode: yeu cau giai ma */
#define OPCODE_DATA    2   /* Opcode: gui/nhan du lieu file */
#define OPCODE_ERROR   3   /* Opcode: bao loi */

/* Header cua moi message: opcode (1 byte) + length (2 byte), khong padding */
typedef struct __attribute__((packed)) {
    unsigned char opcode;
    unsigned short length;
} MessageHeader;

/* Cau truc tham so truyen cho moi thread client */
typedef struct {
    int socket;
} ClientArg;

/* Nhan du lieu day du (dam bao nhan het len bytes) */
int recv_all(int sock, char *buf, int len) {
    int total = 0;
    while (total < len) {
        int n = recv(sock, buf + total, len - total, 0);
        if (n <= 0) return -1;
        total += n;
    }
    return total;
}

/* Gui du lieu day du (dam bao gui het len bytes) */
int send_all(int sock, const char *buf, int len) {
    int total = 0;
    while (total < len) {
        int n = send(sock, buf + total, len - total, 0);
        if (n < 0) return -1;
        total += n;
    }
    return total;
}

/* Gui message co header (opcode + length) va payload */
void send_message(int sock, unsigned char opcode, const char *payload, unsigned short length) {
    MessageHeader hdr;
    hdr.opcode = opcode;
    hdr.length = htons(length);
    send_all(sock, (char *)&hdr, sizeof(hdr));
    if (length > 0 && payload != NULL) {
        send_all(sock, payload, length);
    }
}

/* Ham xu ly cho moi client - chay trong thread rieng */
void *client_handler(void *arg) {
    ClientArg *ca = (ClientArg *)arg;
    int client_socket = ca->socket;
    free(ca);

    char *buffer = NULL;
    char temp_path[] = "/tmp/caesar_temp_XXXXXX";
    char result_path[sizeof(temp_path) + 8];

    /* Nhan header yeu cau (opcode + do dai key) */
    MessageHeader hdr;
    if (recv_all(client_socket, (char *)&hdr, sizeof(hdr)) < 0) {
        close(client_socket);
        return NULL;
    }
    hdr.length = ntohs(hdr.length);

    /* Kiem tra opcode hop le (encrypt hoac decrypt) */
    unsigned char opcode_request = hdr.opcode;
    if (opcode_request != OPCODE_ENCRYPT && opcode_request != OPCODE_DECRYPT) {
        send_message(client_socket, OPCODE_ERROR, NULL, 0);
        close(client_socket);
        return NULL;
    }

    /* Nhan key ma hoa (1 byte) */
    char key_buf[4];
    if (recv_all(client_socket, key_buf, hdr.length) < 0) {
        close(client_socket);
        return NULL;
    }
    unsigned char key = (unsigned char)key_buf[0];

    /* Tao file tam de luu du lieu nhan tu client */
    snprintf(result_path, sizeof(result_path), "%s.res", temp_path);

    int temp_fd = mkstemp(temp_path);
    if (temp_fd < 0) {
        send_message(client_socket, OPCODE_ERROR, NULL, 0);
        close(client_socket);
        return NULL;
    }

    FILE *temp_fp = fdopen(temp_fd, "wb");
    if (temp_fp == NULL) {
        close(temp_fd);
        remove(temp_path);
        send_message(client_socket, OPCODE_ERROR, NULL, 0);
        close(client_socket);
        return NULL;
    }

    buffer = (char *)malloc(BUFFER_SIZE);
    if (buffer == NULL) {
        send_message(client_socket, OPCODE_ERROR, NULL, 0);
        fclose(temp_fp);
        remove(temp_path);
        close(client_socket);
        return NULL;
    }

    /* Nhan du lieu file tu client va ghi vao file tam */
    while (1) {
        /* Nhan header cua moi data message */
        if (recv_all(client_socket, (char *)&hdr, sizeof(hdr)) < 0) {
            fclose(temp_fp);
            remove(temp_path);
            goto cleanup;
        }
        hdr.length = ntohs(hdr.length);

        /* Opcode DATA + length 0 = ket thuc file */
        if (hdr.opcode == OPCODE_DATA && hdr.length == 0) {
            break;
        }

        /* Kiem tra opcode khong hop le */
        if (hdr.opcode != OPCODE_DATA || hdr.length == 0) {
            fclose(temp_fp);
            remove(temp_path);
            send_message(client_socket, OPCODE_ERROR, NULL, 0);
            goto cleanup;
        }

        /* Nhan payload data */
        char *data = (char *)malloc(hdr.length);
        if (data == NULL) {
            fclose(temp_fp);
            remove(temp_path);
            send_message(client_socket, OPCODE_ERROR, NULL, 0);
            goto cleanup;
        }

        if (recv_all(client_socket, data, hdr.length) < 0) {
            free(data);
            fclose(temp_fp);
            remove(temp_path);
            goto cleanup;
        }

        fwrite(data, 1, hdr.length, temp_fp);
        free(data);
    }

    fclose(temp_fp);

    /* Doc file tam, ma hoa/giai ma Caesar, ghi vao file ket qua */
    temp_fp = fopen(temp_path, "rb");
    FILE *result_fp = fopen(result_path, "wb");
    if (temp_fp == NULL || result_fp == NULL) {
        if (temp_fp) fclose(temp_fp);
        if (result_fp) fclose(result_fp);
        remove(temp_path);
        send_message(client_socket, OPCODE_ERROR, NULL, 0);
        goto cleanup;
    }

    /* Vong lap ma hoa/giai ma tung buffer */
    while (1) {
        int bytes_read = (int)fread(buffer, 1, BUFFER_SIZE, temp_fp);
        if (bytes_read <= 0) break;

        /* Ma hoa Caesar: encrypt = (m + key) % 256, decrypt = (m - key) % 256 */
        for (int i = 0; i < bytes_read; i++) {
            unsigned char m = (unsigned char)buffer[i];
            unsigned char c;
            if (opcode_request == OPCODE_ENCRYPT) {
                c = (m + key) % 256;
            } else {
                c = (m - key) % 256;
            }
            buffer[i] = (char)c;
        }

        fwrite(buffer, 1, bytes_read, result_fp);
    }

    fclose(temp_fp);
    fclose(result_fp);

    /* Doc file ket qua va gui ve client theo tung message */
    result_fp = fopen(result_path, "rb");
    if (result_fp == NULL) {
        remove(temp_path);
        remove(result_path);
        send_message(client_socket, OPCODE_ERROR, NULL, 0);
        goto cleanup;
    }

    /* Gui file ket qua ve client, ket thuc bang DATA length 0 */
    while (1) {
        int bytes_read = (int)fread(buffer, 1, BUFFER_SIZE, result_fp);
        if (bytes_read <= 0) {
            send_message(client_socket, OPCODE_DATA, NULL, 0);
            break;
        }
        send_message(client_socket, OPCODE_DATA, buffer, (unsigned short)bytes_read);
    }

    fclose(result_fp);
    remove(temp_path);
    remove(result_path);
    printf("Processed %s request with key %d\n",
           opcode_request == OPCODE_ENCRYPT ? "encrypt" : "decrypt", key);

cleanup:
    /* Don dep tai nguyen */
    free(buffer);
    close(client_socket);
    return NULL;
}

int main(int argc, char *argv[]) {
    /* Kiem tra tham so dong lenh: -p <Port> */
    if (argc != 3 || strcmp(argv[1], "-p") != 0) {
        printf("Usage: %s -p <PortNumber>\n", argv[0]);
        return 1;
    }

    int port = atoi(argv[2]);
    if (port <= 0 || port > 65535) {
        printf("Invalid port number\n");
        return 1;
    }

    /* Tao socket TCP server */
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        printf("Socket creation failed\n");
        return 1;
    }

    /* Cho phep reuse dia chi port */
    int opt = 1;
    setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    /* Bind socket vao port */
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        printf("Bind failed\n");
        close(server_socket);
        return 1;
    }

    /* Lang nghe ket noi, hang doi toi da 5 */
    if (listen(server_socket, 5) < 0) {
        printf("Listen failed\n");
        close(server_socket);
        return 1;
    }

    printf("Caesar Cipher Server is running on port %d\n", port);

    /* Vong lap chap nhan ket noi - moi client tao 1 thread rieng */
    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_addr_len = sizeof(client_addr);
        int client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_addr_len);
        if (client_socket < 0) {
            printf("Accept failed\n");
            continue;
        }

        char client_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, INET_ADDRSTRLEN);
        printf("Client connected from %s\n", client_ip);

        /* Tao thread moi cho client nay */
        ClientArg *ca = (ClientArg *)malloc(sizeof(ClientArg));
        if (ca == NULL) {
            printf("Failed to allocate client arg\n");
            close(client_socket);
            continue;
        }
        ca->socket = client_socket;

        pthread_t thread;
        if (pthread_create(&thread, NULL, client_handler, ca) != 0) {
            printf("Failed to create thread\n");
            close(client_socket);
            free(ca);
        } else {
            pthread_detach(thread);
        }
    }

    close(server_socket);
    return 0;
}
