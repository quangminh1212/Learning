#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

// Kiểm tra xem chuỗi có phải là địa chỉ IP hợp lệ không
int is_valid_ip(const char *str) {
    struct sockaddr_in sa;
    int result = inet_pton(AF_INET, str, &(sa.sin_addr));
    return result == 1;
}

// Kiểm tra xem chuỗi có phải là địa chỉ IPv6 hợp lệ không
int is_valid_ipv6(const char *str) {
    struct sockaddr_in6 sa;
    int result = inet_pton(AF_INET6, str, &(sa.sin6_addr));
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
void resolve_ip_to_hostname(const char *ip_str) {
    struct in_addr addr;
    
    if (inet_pton(AF_INET, ip_str, &addr) != 1) {
        printf("Invalid address\n");
        return;
    }
    
    // Kiểm tra địa chỉ đặc biệt
    if (is_special_ip(ip_str)) {
        printf("special IP address -- may not have DNS record\n");
    }
    
    struct hostent *host = gethostbyaddr(&addr, sizeof(addr), AF_INET);
    
    if (host == NULL) {
        printf("Not found information\n");
        return;
    }
    
    printf("Official name: %s\n", host->h_name);
    
    // In danh sách alias
    if (host->h_aliases != NULL && host->h_aliases[0] != NULL) {
        printf("Alias name:");
        for (int i = 0; host->h_aliases[i] != NULL; i++) {
            printf(" %s", host->h_aliases[i]);
        }
        printf("\n");
    }
}

// Tra cứu địa chỉ IP từ tên miền
void resolve_hostname_to_ip(const char *hostname) {
    struct hostent *host = gethostbyname(hostname);
    
    if (host == NULL) {
        printf("Not found information\n");
        return;
    }
    
    // In địa chỉ IP chính thức
    if (host->h_addr_list != NULL && host->h_addr_list[0] != NULL) {
        char ip_str[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, host->h_addr_list[0], ip_str, INET_ADDRSTRLEN);
        printf("Official IP: %s\n", ip_str);
    }
    
    // In danh sách IP alias
    if (host->h_addr_list != NULL && host->h_addr_list[1] != NULL) {
        printf("Alias IP:");
        for (int i = 1; host->h_addr_list[i] != NULL; i++) {
            char ip_str[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, host->h_addr_list[i], ip_str, INET_ADDRSTRLEN);
            printf(" %s", ip_str);
        }
        printf("\n");
    }
}

int main(int argc, char *argv[]) {
    WSADATA wsa_data;
    if (WSAStartup(MAKEWORD(2, 2), &wsa_data) != 0) {
        printf("WSAStartup failed\n");
        return 1;
    }

    if (argc != 2) {
        printf("Usage: %s <domain_or_ip>\n", argv[0]);
        WSACleanup();
        return 1;
    }
    
    char *parameter = argv[1];
    
    // Kiểm tra xem parameter có phải là địa chỉ IP không
    if (is_valid_ip(parameter)) {
        resolve_ip_to_hostname(parameter);
    } else {
        // Coi là tên miền
        resolve_hostname_to_ip(parameter);
    }
    
    WSACleanup();
    return 0;
}
