#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdint.h>

#define BUFFER_SIZE 8192    /* Kich thuoc buffer nhan file */
#define SHARED_DIR "shared" /* Thu muc luu file upload */

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
    /* Kiem tra cu phap: server -p <Port> */
    if (argc != 3 || strcmp(argv[1], "-p") != 0) {
        printf("Usage: %s -p <PortNumber>\n", argv[0]);
        return 1;
    }

    int port = atoi(argv[2]);
    if (port <= 0 || port > 65535) {
        printf("Invalid port number\n");
        return 1;
    }

    /* Tao thu muc shared neu chua co */
    mkdir(SHARED_DIR, 0777);

    /* Tao socket TCP */
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        printf("Socket creation failed\n");
        return 1;
    }

    /* Cau hinh dia chi server: IP bat ky + port tu tham so */
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    /* Gan socket voi port */
    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        printf("Bind failed\n");
        close(server_socket);
        return 1;
    }

    /* Lang nghe toi da 5 ket noi cho doi */
    if (listen(server_socket, 5) < 0) {
        printf("Listen failed\n");
        close(server_socket);
        return 1;
    }

    printf("Server running on port %d\n", port);

    /* Vong lap vo han: chap nhan va xu ly tung client */
    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_addr_len = sizeof(client_addr);
        int client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_addr_len);
        if (client_socket < 0) {
            printf("Accept failed\n");
            continue;
        }

        /* Buoc 1: Nhan do dai ten file (4 bytes) */
        uint32_t filename_len_net;
        if (recv_all(client_socket, (char *)&filename_len_net, sizeof(filename_len_net)) != sizeof(filename_len_net)) {
            close(client_socket);
            continue;
        }
        uint32_t filename_len = ntohl(filename_len_net);
        if (filename_len == 0 || filename_len >= 1024) {
            close(client_socket);
            continue;
        }

        /* Nhan ten file */
        char *filename = (char *)malloc(filename_len + 1);
        if (filename == NULL || recv_all(client_socket, filename, filename_len) != (ssize_t)filename_len) {
            free(filename);
            close(client_socket);
            continue;
        }
        filename[filename_len] = '\0';

        /* Tao duong dan day du trong thu muc shared */
        char filepath[1024];
        snprintf(filepath, sizeof(filepath), "%s/%s", SHARED_DIR, filename);

        /* Kiem tra file da ton tai chua -> bao loi neu trung */
        if (access(filepath, F_OK) == 0) {
            char *err = "ERROR: File already exists";
            send_all(client_socket, err, strlen(err));
            free(filename);
            close(client_socket);
            continue;
        }

        /* Gui phan hoi OK cho phep upload */
        if (send_all(client_socket, "OK", 2) < 0) {
            free(filename);
            close(client_socket);
            continue;
        }

        /* Buoc 2: Nhan kich thuoc file (8 bytes) */
        long long filesize;
        if (recv_all(client_socket, (char *)&filesize, sizeof(filesize)) != sizeof(filesize)) {
            free(filename);
            close(client_socket);
            continue;
        }

        /* Mo file de ghi nhi phan */
        FILE *fp = fopen(filepath, "wb");
        if (fp == NULL) {
            char *err = "ERROR: Cannot create file";
            send_all(client_socket, err, strlen(err));
            free(filename);
            close(client_socket);
            continue;
        }

        /* Buoc 3: Nhan noi dung file va ghi vao dia */
        char *buffer = (char *)malloc(BUFFER_SIZE);
        ssize_t bytes_received;
        long long received = 0;
        while (received < filesize) {
            int to_read = (filesize - received < BUFFER_SIZE) ? (int)(filesize - received) : BUFFER_SIZE;
            bytes_received = recv_all(client_socket, buffer, to_read);
            if (bytes_received <= 0) break;
            fwrite(buffer, 1, bytes_received, fp);
            received += bytes_received;
        }

        fclose(fp);
        free(buffer);

        /* Buoc 4: Kiem tra va thong bao ket qua */
        if (received == filesize) {
            send_all(client_socket, "SUCCESS", 7);
            printf("Received: %s (%lld bytes)\n", filename, filesize);
        } else {
            send_all(client_socket, "ERROR: Transfer incomplete", 25);
            remove(filepath); /* Xoa file bi loi */
        }

        free(filename);
        close(client_socket);
    }

    close(server_socket);
    return 0;
}
