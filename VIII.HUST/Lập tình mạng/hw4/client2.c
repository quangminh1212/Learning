#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

#define BUFFER_SIZE 4096

int main(int argc, char *argv[]) {
    WSADATA wsa_data;
    if (WSAStartup(MAKEWORD(2, 2), &wsa_data) != 0) {
        printf("WSAStartup failed\n");
        return 1;
    }

    if (argc != 3) {
        printf("Usage: %s <IPAddress> <PortNumber>\n", argv[0]);
        WSACleanup();
        return 1;
    }

    char *server_ip = argv[1];
    int port = atoi(argv[2]);
    
    if (port <= 0 || port > 65535) {
        printf("Invalid port number\n");
        WSACleanup();
        return 1;
    }

    SOCKET client_socket;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];
    char filepath[BUFFER_SIZE];
    
    // Tạo TCP socket
    client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket == INVALID_SOCKET) {
        printf("Socket creation failed\n");
        WSACleanup();
        return 1;
    }

    // Cấu hình server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    inet_pton(AF_INET, server_ip, &server_addr.sin_addr);

    // Kết nối đến server
    if (connect(client_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        printf("Connection failed\n");
        closesocket(client_socket);
        WSACleanup();
        return 1;
    }

    printf("Connected to file server %s:%d\n", server_ip, port);
    printf("Enter file path (empty to exit):\n");

    while (1) {
        printf("> ");
        if (fgets(filepath, BUFFER_SIZE, stdin) == NULL) {
            break;
        }

        // Xóa newline
        filepath[strcspn(filepath, "\n")] = '\0';

        // Nếu xâu rỗng thì thoát
        if (strlen(filepath) == 0) {
            printf("Exiting...\n");
            break;
        }

        // Lấy tên file từ đường dẫn
        char *filename = strrchr(filepath, '\\');
        if (filename == NULL) {
            filename = strrchr(filepath, '/');
        }
        if (filename == NULL) {
            filename = filepath;
        } else {
            filename++; // Bỏ qua ký tự '/' hoặc '\'
        }

        // Kiểm tra file có tồn tại không
        FILE *file = fopen(filepath, "rb");
        if (file == NULL) {
            char response[] = "Error: File not found";
            int response_len = strlen(response);
            send(client_socket, (char*)&response_len, sizeof(int), 0);
            send(client_socket, response, response_len, 0);
            printf("Error: File not found\n");
            continue;
        }

        // Lấy kích thước file
        fseek(file, 0, SEEK_END);
        long file_size = ftell(file);
        fseek(file, 0, SEEK_SET);

        // Gửi độ dài tên file
        int filename_len = strlen(filename);
        send(client_socket, (char*)&filename_len, sizeof(int), 0);
        
        // Gửi tên file
        send(client_socket, filename, filename_len, 0);

        // Nhận phản hồi từ server
        int response_len;
        int bytes_received = recv(client_socket, (char*)&response_len, sizeof(int), 0);
        if (bytes_received <= 0) {
            fclose(file);
            printf("Server disconnected\n");
            break;
        }

        bytes_received = recv(client_socket, buffer, response_len, 0);
        if (bytes_received <= 0) {
            fclose(file);
            printf("Server disconnected\n");
            break;
        }
        buffer[bytes_received] = '\0';

        if (strcmp(buffer, "OK") != 0) {
            printf("%s\n", buffer);
            fclose(file);
            continue;
        }

        // Gửi kích thước file
        send(client_socket, (char*)&file_size, sizeof(long), 0);

        // Gửi nội dung file
        long total_sent = 0;
        while (total_sent < file_size) {
            int to_send = BUFFER_SIZE;
            if (file_size - total_sent < BUFFER_SIZE) {
                to_send = file_size - total_sent;
            }

            size_t bytes_read = fread(buffer, 1, to_send, file);
            if (bytes_read == 0) {
                break;
            }

            int sent = send(client_socket, buffer, bytes_read, 0);
            if (sent <= 0) {
                fclose(file);
                printf("Error: File tranfering is interupted\n");
                break;
            }

            total_sent += sent;
        }

        fclose(file);

        // Nhận kết quả cuối cùng
        bytes_received = recv(client_socket, (char*)&response_len, sizeof(int), 0);
        if (bytes_received <= 0) {
            printf("Server disconnected\n");
            break;
        }

        bytes_received = recv(client_socket, buffer, response_len, 0);
        if (bytes_received <= 0) {
            printf("Server disconnected\n");
            break;
        }
        buffer[bytes_received] = '\0';

        printf("%s\n", buffer);
    }

    closesocket(client_socket);
    WSACleanup();
    return 0;
}
