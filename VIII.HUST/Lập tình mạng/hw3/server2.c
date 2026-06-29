#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

#define BUFFER_SIZE 2048

// Kiểm tra xem chuỗi có phải là địa chỉ IP hợp lệ không
int is_valid_ip(const char *str) {
    struct sockaddr_in sa;
    int result = inet_pton(AF_INET, str, &(sa.sin_addr));
    return result == 1;
}

// Kiểm tra xem địa chỉ IP có phải là địa chỉ đặc biệt không
int is_special_ip(const char *ip_str) {
    struct in_addr addr;
    if (inet_pton(AF_INET, ip_str, &addr) != 1) {
        return 0;
    }
    
    unsigned int ip = ntohl(addr.s_addr);
    
    // Loopback: 127.0.0.0/8
    if ((ip & 0xFF000000) == 0x7F000000) {
        return 1;
    }
    
    // Private: 10.0.0.0/8
    if ((ip & 0xFF000000) == 0x0A000000) {
        return 1;
    }
    
    // Private: 172.16.0.0/12
    if ((ip & 0xFFF00000) == 0xAC100000) {
        return 1;
    }
    
    // Private: 192.168.0.0/16
    if ((ip & 0xFFFF0000) == 0xC0A80000) {
        return 1;
    }
    
    // Link-local: 169.254.0.0/16
    if ((ip & 0xFFFF0000) == 0xA9FE0000) {
        return 1;
    }
    
    // Multicast: 224.0.0.0/4
    if ((ip & 0xF0000000) == 0xE0000000) {
        return 1;
    }
    
    return 0;
}

// Tra cứu tên miền từ địa chỉ IP
void resolve_ip_to_hostname(const char *ip_str, char *response) {
    struct in_addr addr;
    
    if (inet_pton(AF_INET, ip_str, &addr) != 1) {
        strcpy(response, "IP Address is invalid");
        return;
    }
    
    // Kiểm tra địa chỉ đặc biệt
    if (is_special_ip(ip_str)) {
        strcpy(response, "special IP address -- may not have DNS record");
        return;
    }
    
    struct hostent *host = gethostbyaddr(&addr, sizeof(addr), AF_INET);
    
    if (host == NULL) {
        strcpy(response, "Not found information");
        return;
    }
    
    sprintf(response, "Official name: %s", host->h_name);
    
    // In danh sách alias
    if (host->h_aliases != NULL && host->h_aliases[0] != NULL) {
        strcat(response, "\nAlias name:");
        for (int i = 0; host->h_aliases[i] != NULL; i++) {
            strcat(response, " ");
            strcat(response, host->h_aliases[i]);
        }
    }
}

// Tra cứu địa chỉ IP từ tên miền
void resolve_hostname_to_ip(const char *hostname, char *response) {
    struct hostent *host = gethostbyname(hostname);
    
    if (host == NULL) {
        strcpy(response, "Not found information");
        return;
    }
    
    // In địa chỉ IP chính thức
    if (host->h_addr_list != NULL && host->h_addr_list[0] != NULL) {
        char ip_str[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, host->h_addr_list[0], ip_str, INET_ADDRSTRLEN);
        sprintf(response, "Official IP: %s", ip_str);
    }
    
    // In danh sách IP alias
    if (host->h_addr_list != NULL && host->h_addr_list[1] != NULL) {
        strcat(response, "\nAlias IP:");
        for (int i = 1; host->h_addr_list[i] != NULL; i++) {
            char ip_str[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, host->h_addr_list[i], ip_str, INET_ADDRSTRLEN);
            strcat(response, " ");
            strcat(response, ip_str);
        }
    }
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

    printf("DNS Server is running on port %d\n", port);

    while (1) {
        // Nhận dữ liệu từ client
        int bytes_received = recvfrom(server_socket, buffer, BUFFER_SIZE - 1, 0, 
                                      (struct sockaddr*)&client_addr, &client_addr_len);
        if (bytes_received == SOCKET_ERROR) {
            printf("recvfrom failed\n");
            continue;
        }

        buffer[bytes_received] = '\0';
        
        char response[BUFFER_SIZE] = {0};
        
        // Kiểm tra xem có phải là địa chỉ IP không
        if (is_valid_ip(buffer)) {
            resolve_ip_to_hostname(buffer, response);
        } else {
            // Coi là tên miền
            resolve_hostname_to_ip(buffer, response);
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
