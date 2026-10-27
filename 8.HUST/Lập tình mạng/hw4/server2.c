#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

#define BUFFER_SIZE 4096
#define UPLOAD_DIR "uploads"

int file_exists(const char *filename) {
    FILE *file = fopen(filename, "rb");
    if (file) {
        fclose(file);
        return 1;
    }
    return 0;
}

int main(int argc, char *argv[]) {
    WSADATA wsa_data;
    if (WSAStartup(MAKEWORD(2, 2), &wsa_data) != 0) {
        printf("WSAStartup failed\n");
        return 1;
    }

    if (argc != 2) {
        printf("Usage: %s <PortNumber>\n", argv[0]);
        WSACleanup();
        return 1;
    }

    int port = atoi(argv[1]);
    if (port <= 0 || port > 65535) {
        printf("Invalid port number\n");
        WSACleanup();
        return 1;
    }

    // Tạo thư mục uploads
    CreateDirectoryA(UPLOAD_DIR, NULL);

    SOCKET server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    int client_addr_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];
    
    // Tạo TCP socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == INVALID_SOCKET) {
        printf("Socket creation failed\n");
        WSACleanup();
        return 1;
    }

    // Bind socket
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);
    
    if (bind(server_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        printf("Bind failed\n");
        closesocket(server_socket);
        WSACleanup();
        return 1;
    }

    // Listen
    if (listen(server_socket, 5) == SOCKET_ERROR) {
        printf("Listen failed\n");
        closesocket(server_socket);
        WSACleanup();
        return 1;
    }

    printf("File Server is running on port %d\n", port);
    printf("Upload directory: %s\n", UPLOAD_DIR);

    while (1) {
        // Accept connection
        client_socket = accept(server_socket, (struct sockaddr*)&client_addr, &client_addr_len);
        if (client_socket == INVALID_SOCKET) {
            printf("Accept failed\n");
            continue;
        }

        printf("Client connected\n");

        while (1) {
            // Nhận độ dài tên file
            int filename_len;
            int bytes_received = recv(client_socket, (char*)&filename_len, sizeof(int), 0);
            if (bytes_received <= 0) {
                break;
            }

            // Nhận tên file
            char filename[BUFFER_SIZE];
            bytes_received = recv(client_socket, filename, filename_len, 0);
            if (bytes_received <= 0) {
                break;
            }
            filename[bytes_received] = '\0';

            // Kiểm tra xâu rỗng
            if (strlen(filename) == 0) {
                break;
            }

            // Tạo đường dẫn đầy đủ
            char filepath[BUFFER_SIZE];
            sprintf(filepath, "%s/%s", UPLOAD_DIR, filename);

            // Kiểm tra file đã tồn tại
            if (file_exists(filepath)) {
                char response[] = "Error: File is existent on server";
                int response_len = strlen(response);
                send(client_socket, (char*)&response_len, sizeof(int), 0);
                send(client_socket, response, response_len, 0);
                printf("File already exists: %s\n", filename);
                continue;
            }

            // Gửi OK để nhận file
            char ok_msg[] = "OK";
            int ok_len = strlen(ok_msg);
            send(client_socket, (char*)&ok_len, sizeof(int), 0);
            send(client_socket, ok_msg, ok_len, 0);

            // Nhận kích thước file
            long file_size;
            bytes_received = recv(client_socket, (char*)&file_size, sizeof(long), 0);
            if (bytes_received <= 0) {
                break;
            }

            // Mở file để ghi
            FILE *file = fopen(filepath, "wb");
            if (file == NULL) {
                char response[] = "Error: Cannot create file";
                int response_len = strlen(response);
                send(client_socket, (char*)&response_len, sizeof(int), 0);
                send(client_socket, response, response_len, 0);
                printf("Cannot create file: %s\n", filename);
                continue;
            }

            // Nhận nội dung file
            long total_received = 0;
            while (total_received < file_size) {
                int to_receive = BUFFER_SIZE;
                if (file_size - total_received < BUFFER_SIZE) {
                    to_receive = file_size - total_received;
                }

                bytes_received = recv(client_socket, buffer, to_receive, 0);
                if (bytes_received <= 0) {
                    fclose(file);
                    remove(filepath);
                    printf("File transfer interrupted: %s\n", filename);
                    break;
                }

                fwrite(buffer, 1, bytes_received, file);
                total_received += bytes_received;
            }

            fclose(file);

            if (total_received == file_size) {
                char response[] = "Successful transfering";
                int response_len = strlen(response);
                send(client_socket, (char*)&response_len, sizeof(int), 0);
                send(client_socket, response, response_len, 0);
                printf("File received successfully: %s (%ld bytes)\n", filename, file_size);
            } else {
                char response[] = "Error: File tranfering is interupted";
                int response_len = strlen(response);
                send(client_socket, (char*)&response_len, sizeof(int), 0);
                send(client_socket, response, response_len, 0);
                remove(filepath);
            }
        }

        closesocket(client_socket);
        printf("Client disconnected\n");
    }

    closesocket(server_socket);
    WSACleanup();
    return 0;
}
