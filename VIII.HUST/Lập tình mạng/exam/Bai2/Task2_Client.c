/*
 * Task2_Client.c - Client ma hoa/giai ma Caesar - POSIX/Linux
 * Cu phap: client -a <IPAddress> -p <PortNumber>
 * Client chon encrypt/decrypt + key -> gui file -> nhan ket qua -> luu file output
 * Compile tren Ubuntu: gcc -o client Task2_Client.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define BUFFER_SIZE 8192   /* Kich thuoc buffer doc/ghi file */
#define OPCODE_ENCRYPT 0   /* Opcode: yeu cau ma hoa */
#define OPCODE_DECRYPT 1   /* Opcode: yeu cau giai ma */
#define OPCODE_DATA    2   /* Opcode: gui/nhan du lieu file */
#define OPCODE_ERROR   3   /* Opcode: bao loi */

/* Header cua moi message: opcode (1 byte) + length (2 byte), khong padding */
typedef struct __attribute__((packed)) {
    unsigned char opcode;
    unsigned short length;
} MessageHeader;

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

int main(int argc, char *argv[]) {
    /* Parse tham so dong lenh: -a <IP> -p <Port> */
    char server_ip[64] = "";
    int port = 0;

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
    if (inet_pton(AF_INET, server_ip, &server_addr.sin_addr) <= 0) {
        printf("Invalid IP address: %s\n", server_ip);
        close(client_socket);
        return 1;
    }

    if (connect(client_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        printf("Connection failed\n");
        close(client_socket);
        return 1;
    }

    printf("Connected to server %s:%d\n", server_ip, port);

    /* Nhap lua chon: 0 = encrypt, 1 = decrypt */
    int choice;
    printf("Choose operation:\n");
    printf("  0 - Encrypt\n");
    printf("  1 - Decrypt\n");
    printf("Enter choice: ");
    if (scanf("%d", &choice) != 1 || (choice != 0 && choice != 1)) {
        printf("Invalid choice\n");
        close(client_socket);
        return 1;
    }

    /* Nhap key ma hoa (0-255) */
    unsigned int key;
    printf("Enter key (0-255): ");
    if (scanf("%u", &key) != 1 || key > 255) {
        printf("Invalid key\n");
        close(client_socket);
        return 1;
    }
    getchar();  /* Doc ky tu newline con lai sau scanf */

    /* Nhap duong dan file can xu ly */
    char filepath[512];
    printf("Enter file path: ");
    if (fgets(filepath, sizeof(filepath), stdin) == NULL) {
        close(client_socket);
        return 0;
    }
    filepath[strcspn(filepath, "\n")] = '\0';  /* Xoa ky tu xuong dong */

    if (strlen(filepath) == 0) {
        printf("No file specified\n");
        close(client_socket);
        return 0;
    }

    /* Mo file de doc theo che do binary */
    FILE *fp = fopen(filepath, "rb");
    if (fp == NULL) {
        printf("Cannot open file: %s\n", filepath);
        close(client_socket);
        return 1;
    }

    /* Gui yeu cau (opcode + key) cho server */
    unsigned char opcode = (choice == 0) ? OPCODE_ENCRYPT : OPCODE_DECRYPT;
    char key_payload = (char)(unsigned char)key;
    send_message(client_socket, opcode, &key_payload, 1);

    char *buffer = (char *)malloc(BUFFER_SIZE);
    if (buffer == NULL) {
        printf("Memory allocation failed\n");
        fclose(fp);
        close(client_socket);
        return 1;
    }

    /* Doc file va gui du lieu cho server theo tung buffer */
    printf("Sending file data to server...\n");
    while (1) {
        int bytes_read = (int)fread(buffer, 1, BUFFER_SIZE, fp);
        if (bytes_read <= 0) {
            send_message(client_socket, OPCODE_DATA, NULL, 0);
            break;
        }
        send_message(client_socket, OPCODE_DATA, buffer, (unsigned short)bytes_read);
    }
    fclose(fp);

    /* Tao ten file output: encrypt -> .enc, decrypt -> .dec */
    char output_path[512];
    const char *ext = strrchr(filepath, '.');

    if (choice == 0) {
        snprintf(output_path, sizeof(output_path), "%s.enc", filepath);
    } else {
        if (ext && strcmp(ext, ".enc") == 0) {
            snprintf(output_path, sizeof(output_path), "%.*s.dec",
                     (int)(strlen(filepath) - 4), filepath);
        } else {
            snprintf(output_path, sizeof(output_path), "%s.dec", filepath);
        }
    }

    /* Mo file output de ghi ket qua */
    FILE *out_fp = fopen(output_path, "wb");
    if (out_fp == NULL) {
        printf("Cannot create output file: %s\n", output_path);
        free(buffer);
        close(client_socket);
        return 1;
    }

    /* Nhan ket qua tu server va ghi vao file output */
    printf("Receiving result from server...\n");
    int has_error = 0;
    long long total_received = 0;

    while (1) {
        /* Nhan header cua moi response message */
        MessageHeader hdr;
        if (recv_all(client_socket, (char *)&hdr, sizeof(hdr)) < 0) {
            printf("Connection lost\n");
            break;
        }
        hdr.length = ntohs(hdr.length);

        /* Xu ly opcode ERROR tu server */
        if (hdr.opcode == OPCODE_ERROR) {
            printf("Server reported an error\n");
            has_error = 1;
            break;
        }

        /* Opcode DATA + length 0 = ket thuc file ket qua */
        if (hdr.opcode == OPCODE_DATA && hdr.length == 0) {
            break;
        }

        if (hdr.opcode != OPCODE_DATA) {
            printf("Unexpected opcode: %d\n", hdr.opcode);
            has_error = 1;
            break;
        }

        /* Nhan payload data va ghi vao file output */
        char *data = (char *)malloc(hdr.length);
        if (data == NULL) {
            printf("Memory allocation failed\n");
            has_error = 1;
            break;
        }

        if (recv_all(client_socket, data, hdr.length) < 0) {
            printf("Connection lost\n");
            free(data);
            has_error = 1;
            break;
        }

        fwrite(data, 1, hdr.length, out_fp);
        total_received += hdr.length;
        free(data);
    }

    fclose(out_fp);
    free(buffer);

    /* Neu co loi -> xoa file output, nguoc lai bao thanh cong */
    if (has_error) {
        remove(output_path);
        printf("Operation failed\n");
    } else {
        printf("Operation completed successfully\n");
        printf("Output file: %s (%lld bytes)\n", output_path, total_received);
    }

    /* Don dep tai nguyen */
    close(client_socket);
    return 0;
}
