#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdint.h>

#define BUFFER_SIZE 8192   /* Kich thuoc buffer doc file */

/* Gui du so byte qua socket (send co the gui khong het 1 lan) */
ssize_t send_all(int sock, const char *buf, size_t len) {
    size_t total = 0;
    while (total < len) {
        ssize_t s = send(sock, buf + total, len - total, 0);
        if (s < 0) return -1;
        total += s;
    }
    return (ssize_t)total;
}

/* Nhan du so byte tu socket (recv co the tra ve it hon yeu cau) */
ssize_t recv_all(int sock, char *buf, size_t len) {
    size_t total = 0;
    while (total < len) {
        ssize_t r = recv(sock, buf + total, len - total, 0);
        if (r <= 0) return (total > 0) ? (ssize_t)total : r;
        total += r;
    }
    return (ssize_t)total;
}

int main(int argc, char *argv[]) {
    char server_ip[64] = "";
    int port = 0;

    /* Parse tham so dong lenh: -a <IP> -p <Port> */
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-a") == 0 && i + 1 < argc) {
            strncpy(server_ip, argv[++i], sizeof(server_ip) - 1);
        } else if (strcmp(argv[i], "-p") == 0 && i + 1 < argc) {
            port = atoi(argv[++i]);
        }
    }

    /* Kiem tra tham so hop le */
    if (strlen(server_ip) == 0 || port <= 0 || port > 65535) {
        printf("Usage: %s -a <IPAddress> -p <PortNumber>\n", argv[0]);
        return 1;
    }

    /* Tao socket TCP */
    int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket < 0) {
        printf("Socket creation failed\n");
        return 1;
    }

    /* Cau hinh dia chi server va ket noi */
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    inet_pton(AF_INET, server_ip, &server_addr.sin_addr);

    if (connect(client_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        printf("Connection failed\n");
        close(client_socket);
        return 1;
    }

    printf("Connected to %s:%d\n", server_ip, port);

    /* Nhap duong dan file tu ban phim */
    char filepath[512];
    printf("Enter file path: ");
    if (fgets(filepath, sizeof(filepath), stdin) == NULL) {
        close(client_socket);
        return 0;
    }
    filepath[strcspn(filepath, "\n")] = '\0';  /* Xoa ky tu xuong dong */

    /* Mo file can upload */
    FILE *fp = fopen(filepath, "rb");
    if (fp == NULL) {
        printf("Cannot open file\n");
        close(client_socket);
        return 1;
    }

    /* Trich xuat ten file tu duong dan (bo qua thu muc) */
    const char *filename = strrchr(filepath, '/');
    if (filename == NULL) filename = strrchr(filepath, '\\');
    if (filename == NULL) filename = filepath;
    else filename++;

    /* Buoc 1: Gui do dai ten file (4 bytes) va ten file cho server */
    uint32_t filename_len = (uint32_t)strlen(filename);
    uint32_t filename_len_net = htonl(filename_len);
    if (send_all(client_socket, (char *)&filename_len_net, sizeof(filename_len_net)) < 0 ||
        send_all(client_socket, filename, filename_len) < 0) {
        printf("Send filename failed\n");
        fclose(fp);
        close(client_socket);
        return 1;
    }

    /* Nhan phan hoi tu server (OK hoac loi) */
    char response[256];
    ssize_t bytes_received = recv_all(client_socket, response, 2);
    if (bytes_received <= 0) {
        printf("Server disconnected\n");
        fclose(fp);
        close(client_socket);
        return 1;
    }
    response[bytes_received] = '\0';

    if (strncmp(response, "OK", 2) != 0) {
        /* Nhan them phan con lai cua thong bao loi */
        bytes_received = recv_all(client_socket, response + 2, sizeof(response) - 3);
        if (bytes_received > 0) response[2 + bytes_received] = '\0';
        printf("%s\n", response);
        fclose(fp);
        close(client_socket);
        return 1;
    }

    /* Buoc 2: Tinh kich thuoc file va gui cho server */
    fseek(fp, 0, SEEK_END);
    long long filesize = ftello(fp);
    fseek(fp, 0, SEEK_SET);

    if (send_all(client_socket, (char *)&filesize, sizeof(long long)) < 0) {
        printf("Send filesize failed\n");
        fclose(fp);
        close(client_socket);
        return 1;
    }

    /* Buoc 3: Doc file va gui noi dung theo tung buffer */
    char *buffer = (char *)malloc(BUFFER_SIZE);
    long long sent = 0;
    while (sent < filesize) {
        int to_read = (filesize - sent < BUFFER_SIZE) ? (int)(filesize - sent) : BUFFER_SIZE;
        int bytes_read = (int)fread(buffer, 1, to_read, fp);
        if (bytes_read <= 0) break;

        /* Dam bao gui het so byte da doc (send co the gui khong het 1 lan) */
        int total_sent = 0;
        while (total_sent < bytes_read) {
            ssize_t s = send(client_socket, buffer + total_sent, bytes_read - total_sent, 0);
            if (s < 0) {
                printf("Send error\n");
                free(buffer);
                fclose(fp);
                close(client_socket);
                return 1;
            }
            total_sent += s;
        }
        sent += bytes_read;
    }

    free(buffer);
    fclose(fp);

    /* Buoc 4: Nhan ket qua cuoi cung tu server */
    bytes_received = recv_all(client_socket, response, sizeof(response) - 1);
    if (bytes_received > 0) {
        response[bytes_received] = '\0';
        printf("%s\n", response);
    }

    close(client_socket);
    return 0;
}
