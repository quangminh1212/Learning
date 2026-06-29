#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <process.h>
#pragma comment(lib, "ws2_32.lib")

#define BUFFER_SIZE 1024
#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 5500

// Hàm xử lý client trong thread
unsigned __stdcall client_handler(void *arg) {
    SOCKET client_socket = (SOCKET)arg;
    char buffer[BUFFER_SIZE];
    
    printf("Client connected\n");
    
    while (1) {
        // Nhận độ dài xâu
        int msg_len;
        int bytes_received = recv(client_socket, (char*)&msg_len, sizeof(int), 0);
        if (bytes_received <= 0) {
            break;
        }

        // Nhận xâu
        bytes_received = recv(client_socket, buffer, msg_len, 0);
        if (bytes_received <= 0) {
            break;
        }
        buffer[bytes_received] = '\0';
        
        // Kiểm tra lệnh thoát
        if (strcmp(buffer, "q") == 0 || strcmp(buffer, "Q") == 0) {
            printf("Client requested disconnect\n");
            break;
        }
        
        // Chuyển sang viết hoa
        for (int i = 0; buffer[i] != '\0'; i++) {
            buffer[i] = toupper(buffer[i]);
        }
        
        // Gửi độ dài phản hồi
        int response_len = strlen(buffer);
        send(client_socket, (char*)&response_len, sizeof(int), 0);
        
        // Gửi phản hồi
        send(client_socket, buffer, response_len, 0);
        
        printf("Received: %s, Sent: %s\n", buffer, buffer);
    }

    closesocket(client_socket);
    printf("Client disconnected\n");
    return 0;
}

int main() {
    WSADATA wsa_data;
    if (WSAStartup(MAKEWORD(2, 2), &wsa_data) != 0) {
        printf("WSAStartup failed\n");
        return 1;
    }

    SOCKET server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    int client_addr_len = sizeof(client_addr);
    
    // Tạo TCP socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == INVALID_SOCKET) {
        printf("Socket creation failed\n");
        WSACleanup();
        return 1;
    }

    // Bind socket
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr(SERVER_IP);
    server_addr.sin_port = htons(SERVER_PORT);
    
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

    printf("Server is running on %s:%d\n", SERVER_IP, SERVER_PORT);

    while (1) {
        // Accept connection
        client_socket = accept(server_socket, (struct sockaddr*)&client_addr, &client_addr_len);
        if (client_socket == INVALID_SOCKET) {
            printf("Accept failed\n");
            continue;
        }

        // Tạo thread để xử lý client
        HANDLE thread_handle = (HANDLE)_beginthreadex(NULL, 0, client_handler, (void*)client_socket, 0, NULL);
        if (thread_handle == NULL) {
            printf("Failed to create thread\n");
            closesocket(client_socket);
        } else {
            CloseHandle(thread_handle);
        }
    }

    closesocket(server_socket);
    WSACleanup();
    return 0;
}
