#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

#define BUFFER_SIZE 1024
#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 5500

int main() {
    WSADATA wsa_data;
    if (WSAStartup(MAKEWORD(2, 2), &wsa_data) != 0) {
        printf("WSAStartup failed\n");
        return 1;
    }

    SOCKET client_socket;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];
    long total_bytes_sent = 0;
    
    // Tạo TCP socket
    client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket == INVALID_SOCKET) {
        printf("Socket creation failed\n");
        WSACleanup();
        return 1;
    }

    // Cấu hình server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    server_addr.sin_addr.s_addr = inet_addr(SERVER_IP);

    // Kết nối đến server
    if (connect(client_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        printf("Cannot connect to server\n");
        closesocket(client_socket);
        WSACleanup();
        return 1;
    }

    printf("Connected to server %s:%d\n", SERVER_IP, SERVER_PORT);
    printf("Enter message (q or Q to quit):\n");

    while (1) {
        printf("> ");
        if (fgets(buffer, BUFFER_SIZE, stdin) == NULL) {
            break;
        }

        // Xóa newline
        buffer[strcspn(buffer, "\n")] = '\0';

        // Kiểm tra lệnh thoát
        if (strcmp(buffer, "q") == 0 || strcmp(buffer, "Q") == 0) {
            // Gửi lệnh thoát cho server
            int msg_len = strlen(buffer);
            send(client_socket, (char*)&msg_len, sizeof(int), 0);
            send(client_socket, buffer, msg_len, 0);
            total_bytes_sent += msg_len + sizeof(int);
            break;
        }

        // Gửi độ dài xâu
        int msg_len = strlen(buffer);
        send(client_socket, (char*)&msg_len, sizeof(int), 0);
        
        // Gửi xâu
        send(client_socket, buffer, msg_len, 0);
        total_bytes_sent += msg_len + sizeof(int);

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
        printf("Server: %s\n", buffer);
    }

    printf("Total bytes sent: %ld\n", total_bytes_sent);
    closesocket(client_socket);
    WSACleanup();
    return 0;
}
