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
    char userid[50], password[50];
    
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
        printf("Cannot connect to server\n");
        closesocket(client_socket);
        WSACleanup();
        return 1;
    }

    printf("Connected to login server %s:%d\n", server_ip, port);

    // Nhập userid
    printf("Enter userid: ");
    fgets(userid, sizeof(userid), stdin);
    userid[strcspn(userid, "\n")] = '\0';

    // Gửi userid
    int msg_len = strlen(userid);
    send(client_socket, (char*)&msg_len, sizeof(int), 0);
    send(client_socket, userid, msg_len, 0);

    // Nhập password
    printf("Enter password: ");
    fgets(password, sizeof(password), stdin);
    password[strcspn(password, "\n")] = '\0';

    // Gửi password
    msg_len = strlen(password);
    send(client_socket, (char*)&msg_len, sizeof(int), 0);
    send(client_socket, password, msg_len, 0);

    // Nhận kết quả đăng nhập
    int bytes_received = recv(client_socket, (char*)&msg_len, sizeof(int), 0);
    if (bytes_received <= 0) {
        printf("Server disconnected\n");
        closesocket(client_socket);
        WSACleanup();
        return 1;
    }

    bytes_received = recv(client_socket, buffer, msg_len, 0);
    if (bytes_received <= 0) {
        printf("Server disconnected\n");
        closesocket(client_socket);
        WSACleanup();
        return 1;
    }
    buffer[bytes_received] = '\0';

    printf("%s\n", buffer);

    if (strstr(buffer, "Login successful") == NULL) {
        closesocket(client_socket);
        WSACleanup();
        return 0;
    }

    // Menu sau đăng nhập
    printf("\nAvailable commands:\n");
    printf("- info: View your connection info\n");
    printf("- online: View all online users\n");
    printf("- logout: Logout\n");

    while (1) {
        printf("> ");
        if (fgets(buffer, BUFFER_SIZE, stdin) == NULL) {
            break;
        }

        buffer[strcspn(buffer, "\n")] = '\0';

        if (strlen(buffer) == 0) {
            continue;
        }

        // Gửi lệnh
        msg_len = strlen(buffer);
        send(client_socket, (char*)&msg_len, sizeof(int), 0);
        send(client_socket, buffer, msg_len, 0);

        if (strcmp(buffer, "logout") == 0) {
            // Nhận kết quả logout
            bytes_received = recv(client_socket, (char*)&msg_len, sizeof(int), 0);
            if (bytes_received <= 0) break;
            bytes_received = recv(client_socket, buffer, msg_len, 0);
            if (bytes_received <= 0) break;
            buffer[bytes_received] = '\0';
            printf("%s\n", buffer);
            break;
        }

        // Nhận phản hồi
        bytes_received = recv(client_socket, (char*)&msg_len, sizeof(int), 0);
        if (bytes_received <= 0) break;
        bytes_received = recv(client_socket, buffer, msg_len, 0);
        if (bytes_received <= 0) break;
        buffer[bytes_received] = '\0';
        printf("%s\n", buffer);
    }

    closesocket(client_socket);
    WSACleanup();
    return 0;
}
