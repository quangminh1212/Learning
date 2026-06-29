#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

#define MAX_LINE 1024
#define LOG_FILE "resolver.log"

FILE *log_file = NULL;

// Mở file log
void open_log() {
    log_file = fopen(LOG_FILE, "a");
    if (log_file == NULL) {
        perror("Cannot open log file");
    }
}

// Đóng file log
void close_log() {
    if (log_file != NULL) {
        fclose(log_file);
    }
}

// Ghi log
void write_log(const char *message) {
    if (log_file != NULL) {
        time_t now = time(NULL);
        char *time_str = ctime(&now);
        time_str[strlen(time_str) - 1] = '\0'; // Remove newline
        fprintf(log_file, "[%s] %s\n", time_str, message);
        fflush(log_file);
    }
}

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

// Kiểm tra xem địa chỉ IPv6 có phải là địa chỉ đặc biệt không
int is_special_ipv6(const char *ip_str) {
    struct in6_addr addr;
    if (inet_pton(AF_INET6, ip_str, &addr) != 1) {
        return 0;
    }
    
    // Loopback: ::1
    if (addr.s6_addr[15] == 1 && 
        addr.s6_addr[0] == 0 && addr.s6_addr[1] == 0 && 
        addr.s6_addr[2] == 0 && addr.s6_addr[3] == 0 &&
        addr.s6_addr[4] == 0 && addr.s6_addr[5] == 0 && 
        addr.s6_addr[6] == 0 && addr.s6_addr[7] == 0 &&
        addr.s6_addr[8] == 0 && addr.s6_addr[9] == 0 && 
        addr.s6_addr[10] == 0 && addr.s6_addr[11] == 0 &&
        addr.s6_addr[12] == 0 && addr.s6_addr[13] == 0 && 
        addr.s6_addr[14] == 0) {
        return 1;
    }
    
    // Link-local: fe80::/10
    if ((addr.s6_addr[0] & 0xFF) == 0xFE && (addr.s6_addr[1] & 0xC0) == 0x80) {
        return 1;
    }
    
    // Unique local: fc00::/7
    if ((addr.s6_addr[0] & 0xFE) == 0xFC) {
        return 1;
    }
    
    // Multicast: ff00::/8
    if ((addr.s6_addr[0] & 0xFF) == 0xFF) {
        return 1;
    }
    
    return 0;
}

// Tra cứu tên miền từ địa chỉ IP
void resolve_ip_to_hostname(const char *ip_str) {
    struct in_addr addr;
    struct in6_addr addr6;
    int is_ipv6 = 0;
    
    char log_msg[MAX_LINE];
    time_t start_time, end_time;
    double elapsed_time;
    
    start_time = time(NULL);
    
    if (inet_pton(AF_INET, ip_str, &addr) == 1) {
        // IPv4
        if (is_special_ip(ip_str)) {
            printf("special IP address -- may not have DNS record\n");
            snprintf(log_msg, MAX_LINE, "Special IP: %s", ip_str);
            write_log(log_msg);
            return;
        }
        
        struct hostent *host = gethostbyaddr(&addr, sizeof(addr), AF_INET);
        
        if (host == NULL) {
            printf("Not found information\n");
            snprintf(log_msg, MAX_LINE, "Not found: %s", ip_str);
            write_log(log_msg);
            return;
        }
        
        printf("Official name: %s\n", host->h_name);
        
        if (host->h_aliases != NULL && host->h_aliases[0] != NULL) {
            printf("Alias name:");
            for (int i = 0; host->h_aliases[i] != NULL; i++) {
                printf(" %s", host->h_aliases[i]);
            }
            printf("\n");
        }
        
        snprintf(log_msg, MAX_LINE, "IP %s -> %s", ip_str, host->h_name);
        write_log(log_msg);
        
    } else if (inet_pton(AF_INET6, ip_str, &addr6) == 1) {
        // IPv6
        is_ipv6 = 1;
        if (is_special_ipv6(ip_str)) {
            printf("special IPv6 address -- may not have DNS record\n");
            snprintf(log_msg, MAX_LINE, "Special IPv6: %s", ip_str);
            write_log(log_msg);
            return;
        }
        
        struct hostent *host = gethostbyaddr(&addr6, sizeof(addr6), AF_INET6);
        
        if (host == NULL) {
            printf("Not found information\n");
            snprintf(log_msg, MAX_LINE, "Not found: %s", ip_str);
            write_log(log_msg);
            return;
        }
        
        printf("Official name: %s\n", host->h_name);
        
        if (host->h_aliases != NULL && host->h_aliases[0] != NULL) {
            printf("Alias name:");
            for (int i = 0; host->h_aliases[i] != NULL; i++) {
                printf(" %s", host->h_aliases[i]);
            }
            printf("\n");
        }
        
        snprintf(log_msg, MAX_LINE, "IPv6 %s -> %s", ip_str, host->h_name);
        write_log(log_msg);
        
    } else {
        printf("Invalid address\n");
        snprintf(log_msg, MAX_LINE, "Invalid address: %s", ip_str);
        write_log(log_msg);
        return;
    }
    
    end_time = time(NULL);
    elapsed_time = difftime(end_time, start_time);
    printf("Query time: %.2f seconds\n", elapsed_time);
}

// Tra cứu địa chỉ IP từ tên miền
void resolve_hostname_to_ip(const char *hostname) {
    struct hostent *host;
    char log_msg[MAX_LINE];
    time_t start_time, end_time;
    double elapsed_time;
    
    start_time = time(NULL);
    
    host = gethostbyname(hostname);
    
    if (host == NULL) {
        printf("Not found information\n");
        snprintf(log_msg, MAX_LINE, "Not found: %s", hostname);
        write_log(log_msg);
        return;
    }
    
    // In canonical name (CNAME)
    if (host->h_name != NULL) {
        printf("Canonical name: %s\n", host->h_name);
    }
    
    // In địa chỉ IP chính thức
    if (host->h_addr_list != NULL && host->h_addr_list[0] != NULL) {
        if (host->h_addrtype == AF_INET) {
            char ip_str[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, host->h_addr_list[0], ip_str, INET_ADDRSTRLEN);
            printf("Official IP: %s\n", ip_str);
        } else if (host->h_addrtype == AF_INET6) {
            char ip_str[INET6_ADDRSTRLEN];
            inet_ntop(AF_INET6, host->h_addr_list[0], ip_str, INET6_ADDRSTRLEN);
            printf("Official IPv6: %s\n", ip_str);
        }
    }
    
    // In danh sách IP alias
    if (host->h_addr_list != NULL && host->h_addr_list[1] != NULL) {
        if (host->h_addrtype == AF_INET) {
            printf("Alias IP:");
            for (int i = 1; host->h_addr_list[i] != NULL; i++) {
                char ip_str[INET_ADDRSTRLEN];
                inet_ntop(AF_INET, host->h_addr_list[i], ip_str, INET_ADDRSTRLEN);
                printf(" %s", ip_str);
            }
            printf("\n");
        } else if (host->h_addrtype == AF_INET6) {
            printf("Alias IPv6:");
            for (int i = 1; host->h_addr_list[i] != NULL; i++) {
                char ip_str[INET6_ADDRSTRLEN];
                inet_ntop(AF_INET6, host->h_addr_list[i], ip_str, INET6_ADDRSTRLEN);
                printf(" %s", ip_str);
            }
            printf("\n");
        }
    }
    
    snprintf(log_msg, MAX_LINE, "Hostname %s -> resolved", hostname);
    write_log(log_msg);
    
    end_time = time(NULL);
    elapsed_time = difftime(end_time, start_time);
    printf("Query time: %.2f seconds\n", elapsed_time);
}

// Xử lý một chuỗi input
void process_input(const char *input) {
    // Xóa khoảng trắng thừa
    char trimmed[MAX_LINE];
    int i = 0, j = 0;
    while (input[i] != '\0') {
        if (!isspace(input[i])) {
            trimmed[j++] = input[i];
        }
        i++;
    }
    trimmed[j] = '\0';
    
    if (strlen(trimmed) == 0) {
        return;
    }
    
    // Kiểm tra xem có nhiều địa chỉ trên cùng một dòng không
    char *token = strtok(trimmed, " \t");
    while (token != NULL) {
        printf("\nResolving: %s\n", token);
        
        if (is_valid_ip(token)) {
            resolve_ip_to_hostname(token);
        } else if (is_valid_ipv6(token)) {
            resolve_ip_to_hostname(token);
        } else {
            resolve_hostname_to_ip(token);
        }
        
        token = strtok(NULL, " \t");
    }
}

// Chế độ batch: đọc từ file
void batch_mode(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Cannot open file");
        return;
    }
    
    char line[MAX_LINE];
    while (fgets(line, MAX_LINE, file) != NULL) {
        // Xóa newline
        line[strcspn(line, "\n")] = '\0';
        
        if (strlen(line) == 0) {
            continue;
        }
        
        printf("\n--- Batch: %s ---\n", line);
        process_input(line);
    }
    
    fclose(file);
}

int main(int argc, char *argv[]) {
    WSADATA wsa_data;
    if (WSAStartup(MAKEWORD(2, 2), &wsa_data) != 0) {
        printf("WSAStartup failed\n");
        return 1;
    }

    open_log();
    
    if (argc == 2) {
        // Kiểm tra xem tham số có phải là file không
        FILE *test_file = fopen(argv[1], "r");
        if (test_file != NULL) {
            fclose(test_file);
            // Chế độ batch
            printf("Batch mode: reading from %s\n", argv[1]);
            batch_mode(argv[1]);
        } else {
            // Xử lý tham số đơn
            process_input(argv[1]);
        }
    } else if (argc == 1) {
        // Chế độ tương tác
        printf("Interactive mode (enter empty line to exit)\n");
        
        char input[MAX_LINE];
        while (1) {
            printf("\nEnter domain or IP: ");
            if (fgets(input, MAX_LINE, stdin) == NULL) {
                break;
            }
            
            // Xóa newline
            input[strcspn(input, "\n")] = '\0';
            
            if (strlen(input) == 0) {
                printf("Exiting...\n");
                break;
            }
            
            process_input(input);
        }
    } else {
        printf("Usage: %s [domain_or_ip | batch_file]\n", argv[0]);
        close_log();
        WSACleanup();
        return 1;
    }
    
    close_log();
    WSACleanup();
    return 0;
}
