#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

#define BUFFER_SIZE 1024

void process_string(const char *input, char *letters, char *digits, int *has_error) {
    int letter_idx = 0;
    int digit_idx = 0;
    *has_error = 0;
    
    for (int i = 0; input[i] != '\0'; i++) {
        if (isalpha(input[i])) {
            letters[letter_idx++] = input[i];
        } else if (isdigit(input[i])) {
            digits[digit_idx++] = input[i];
        } else {
            *has_error = 1;
        }
    }
    
    letters[letter_idx] = '\0';
    digits[digit_idx] = '\0';
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

    SOCKET server_socket;
    struct sockaddr_in server_addr, client_addr;
    int client_addr_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];
    
    // Tạo UDP socket
    server_socket = socket(AF_INET, SOCK_DGRAM, 0);
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

    printf("Server is running on port %d\n", port);

    while (1) {
        // Nhận dữ liệu từ client
        int bytes_received = recvfrom(server_socket, buffer, BUFFER_SIZE - 1, 0, 
                                      (struct sockaddr*)&client_addr, &client_addr_len);
        if (bytes_received == SOCKET_ERROR) {
            printf("recvfrom failed\n");
            continue;
        }

        buffer[bytes_received] = '\0';
        
        // Xử lý xâu
        char letters[BUFFER_SIZE] = {0};
        char digits[BUFFER_SIZE] = {0};
        int has_error;
        
        process_string(buffer, letters, digits, &has_error);
        
        char response[BUFFER_SIZE];
        if (has_error) {
            strcpy(response, "Error");
        } else {
            sprintf(response, "%s %s", digits, letters);
        }
        
        // Gửi kết quả về client
        sendto(server_socket, response, strlen(response), 0, 
               (struct sockaddr*)&client_addr, client_addr_len);
        
        printf("Received: %s, Sent: %s\n", buffer, response);
    }

    closesocket(server_socket);
    WSACleanup();
    return 0;
}
