#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

#define BUFFER_SIZE 1024

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

    printf("Connected to server %s:%d\n", server_ip, port);
    printf("Enter string (empty to exit):\n");

    while (1) {
        printf("> ");
        if (fgets(buffer, BUFFER_SIZE, stdin) == NULL) {
            break;
        }

        // Xóa newline
        buffer[strcspn(buffer, "\n")] = '\0';

        // Nếu xâu rỗng thì thoát
        if (strlen(buffer) == 0) {
            printf("Exiting...\n");
            break;
        }

        // Gửi độ dài xâu trước (để xử lý vấn đề byte stream của TCP)
        int msg_len = strlen(buffer);
        send(client_socket, (char*)&msg_len, sizeof(int), 0);
        
        // Gửi xâu
        send(client_socket, buffer, msg_len, 0);

        // Nhận độ dài phản hồi
        int response_len;
        int bytes_received = recv(client_socket, (char*)&response_len, sizeof(int), 0);
        if (bytes_received <= 0) {
            printf("Server disconnected\n");
            break;
        }

        // Nhận phản hồi
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
