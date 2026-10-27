#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <process.h>
#include <windows.h>
#pragma comment(lib, "ws2_32.lib")

#define BUFFER_SIZE 1024
#define MAX_ACCOUNTS 100
#define MAX_CLIENTS 50
#define ACCOUNT_FILE "account.txt"

// Cấu trúc tài khoản
typedef struct {
    char userid[50];
    char password[50];
    int status; // 0: bị khóa, 1: hoạt động
    int failed_attempts;
} Account;

// Cấu trúc client đang online
typedef struct {
    char userid[50];
    char ip[INET_ADDRSTRLEN];
    time_t login_time;
    SOCKET socket;
} OnlineClient;

Account accounts[MAX_ACCOUNTS];
OnlineClient online_clients[MAX_CLIENTS];
int account_count = 0;
HANDLE accounts_mutex;
HANDLE online_clients_mutex;

// Đọc file account.txt
void load_accounts() {
    FILE *file = fopen(ACCOUNT_FILE, "r");
    if (file == NULL) {
        printf("Cannot open account file\n");
        return;
    }

    account_count = 0;
    while (fscanf(file, "%s %s %d", accounts[account_count].userid, 
                  accounts[account_count].password, &accounts[account_count].status) == 3) {
        accounts[account_count].failed_attempts = 0;
        account_count++;
        if (account_count >= MAX_ACCOUNTS) break;
    }

    fclose(file);
    printf("Loaded %d accounts\n", account_count);
}

// Lưu file account.txt
void save_accounts() {
    FILE *file = fopen(ACCOUNT_FILE, "w");
    if (file == NULL) {
        printf("Cannot save account file\n");
        return;
    }

    for (int i = 0; i < account_count; i++) {
        fprintf(file, "%s %s %d\n", accounts[i].userid, accounts[i].password, accounts[i].status);
    }

    fclose(file);
}

// Tìm tài khoản theo userid
Account* find_account(const char *userid) {
    for (int i = 0; i < account_count; i++) {
        if (strcmp(accounts[i].userid, userid) == 0) {
            return &accounts[i];
        }
    }
    return NULL;
}

// Thêm client vào danh sách online
void add_online_client(const char *userid, const char *ip, SOCKET socket) {
    WaitForSingleObject(online_clients_mutex, INFINITE);
    
    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (online_clients[i].socket == INVALID_SOCKET) {
            strcpy(online_clients[i].userid, userid);
            strcpy(online_clients[i].ip, ip);
            online_clients[i].login_time = time(NULL);
            online_clients[i].socket = socket;
            break;
        }
    }
    
    ReleaseMutex(online_clients_mutex);
}

// Xóa client khỏi danh sách online
void remove_online_client(SOCKET socket) {
    WaitForSingleObject(online_clients_mutex, INFINITE);
    
    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (online_clients[i].socket == socket) {
            online_clients[i].socket = INVALID_SOCKET;
            break;
        }
    }
    
    ReleaseMutex(online_clients_mutex);
}

// Lấy danh sách online cho một userid
void get_online_info(const char *userid, char *response) {
    WaitForSingleObject(online_clients_mutex, INFINITE);
    
    int count = 0;
    char temp[BUFFER_SIZE];
    strcpy(response, "");
    
    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (online_clients[i].socket != INVALID_SOCKET && 
            strcmp(online_clients[i].userid, userid) == 0) {
            char time_str[100];
            struct tm *tm_info = localtime(&online_clients[i].login_time);
            strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", tm_info);
            
            sprintf(temp, "IP: %s, Login time: %s\n", online_clients[i].ip, time_str);
            strcat(response, temp);
            count++;
        }
    }
    
    if (count == 0) {
        strcpy(response, "No other connections for this account\n");
    }
    
    ReleaseMutex(online_clients_mutex);
}

// Lấy danh sách tất cả user online
void get_all_online_users(char *response) {
    WaitForSingleObject(online_clients_mutex, INFINITE);
    
    char temp[BUFFER_SIZE];
    strcpy(response, "Online users:\n");
    
    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (online_clients[i].socket != INVALID_SOCKET) {
            sprintf(temp, "- %s (IP: %s)\n", online_clients[i].userid, online_clients[i].ip);
            strcat(response, temp);
        }
    }
    
    ReleaseMutex(online_clients_mutex);
}

// Hàm xử lý client trong thread
unsigned __stdcall client_handler(void *arg) {
    SOCKET client_socket = (SOCKET)arg;
    struct sockaddr_in client_addr;
    int addr_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];
    char client_ip[INET_ADDRSTRLEN];
    
    getpeername(client_socket, (struct sockaddr*)&client_addr, &addr_len);
    inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, INET_ADDRSTRLEN);
    
    printf("Client connected from %s\n", client_ip);
    
    // Nhận userid
    int msg_len;
    int bytes_received = recv(client_socket, (char*)&msg_len, sizeof(int), 0);
    if (bytes_received <= 0) {
        closesocket(client_socket);
        return 0;
    }
    
    bytes_received = recv(client_socket, buffer, msg_len, 0);
    if (bytes_received <= 0) {
        closesocket(client_socket);
        return 0;
    }
    buffer[bytes_received] = '\0';
    char userid[50];
    strcpy(userid, buffer);
    
    // Nhận password
    bytes_received = recv(client_socket, (char*)&msg_len, sizeof(int), 0);
    if (bytes_received <= 0) {
        closesocket(client_socket);
        return 0;
    }
    
    bytes_received = recv(client_socket, buffer, msg_len, 0);
    if (bytes_received <= 0) {
        closesocket(client_socket);
        return 0;
    }
    buffer[bytes_received] = '\0';
    char password[50];
    strcpy(password, buffer);
    
    // Kiểm tra đăng nhập
    WaitForSingleObject(accounts_mutex, INFINITE);
    Account *account = find_account(userid);
    
    if (account == NULL) {
        ReleaseMutex(accounts_mutex);
        strcpy(buffer, "Login failed: Account not found");
        msg_len = strlen(buffer);
        send(client_socket, (char*)&msg_len, sizeof(int), 0);
        send(client_socket, buffer, msg_len, 0);
        closesocket(client_socket);
        return 0;
    }
    
    if (account->status == 0) {
        ReleaseMutex(accounts_mutex);
        strcpy(buffer, "Login failed: Account is locked");
        msg_len = strlen(buffer);
        send(client_socket, (char*)&msg_len, sizeof(int), 0);
        send(client_socket, buffer, msg_len, 0);
        closesocket(client_socket);
        return 0;
    }
    
    if (strcmp(account->password, password) != 0) {
        account->failed_attempts++;
        if (account->failed_attempts >= 5) {
            account->status = 0;
            save_accounts();
            ReleaseMutex(accounts_mutex);
            strcpy(buffer, "Login failed: Account locked due to too many failed attempts");
        } else {
            ReleaseMutex(accounts_mutex);
            sprintf(buffer, "Login failed: Wrong password. Attempts left: %d", 5 - account->failed_attempts);
        }
        msg_len = strlen(buffer);
        send(client_socket, (char*)&msg_len, sizeof(int), 0);
        send(client_socket, buffer, msg_len, 0);
        closesocket(client_socket);
        return 0;
    }
    
    // Đăng nhập thành công
    account->failed_attempts = 0;
    ReleaseMutex(accounts_mutex);
    
    add_online_client(userid, client_ip, client_socket);
    
    strcpy(buffer, "Login successful");
    msg_len = strlen(buffer);
    send(client_socket, (char*)&msg_len, sizeof(int), 0);
    send(client_socket, buffer, msg_len, 0);
    
    printf("User %s logged in from %s\n", userid, client_ip);
    
    // Xử lý các lệnh sau đăng nhập
    while (1) {
        bytes_received = recv(client_socket, (char*)&msg_len, sizeof(int), 0);
        if (bytes_received <= 0) break;
        
        bytes_received = recv(client_socket, buffer, msg_len, 0);
        if (bytes_received <= 0) break;
        buffer[bytes_received] = '\0';
        
        if (strcmp(buffer, "logout") == 0) {
            strcpy(buffer, "Logout successful");
            msg_len = strlen(buffer);
            send(client_socket, (char*)&msg_len, sizeof(int), 0);
            send(client_socket, buffer, msg_len, 0);
            break;
        } else if (strcmp(buffer, "info") == 0) {
            get_online_info(userid, buffer);
            msg_len = strlen(buffer);
            send(client_socket, (char*)&msg_len, sizeof(int), 0);
            send(client_socket, buffer, msg_len, 0);
        } else if (strcmp(buffer, "online") == 0) {
            get_all_online_users(buffer);
            msg_len = strlen(buffer);
            send(client_socket, (char*)&msg_len, sizeof(int), 0);
            send(client_socket, buffer, msg_len, 0);
        } else {
            strcpy(buffer, "Unknown command. Available: logout, info, online");
            msg_len = strlen(buffer);
            send(client_socket, (char*)&msg_len, sizeof(int), 0);
            send(client_socket, buffer, msg_len, 0);
        }
    }
    
    remove_online_client(client_socket);
    closesocket(client_socket);
    printf("User %s logged out\n", userid);
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

    // Khởi tạo mutex
    accounts_mutex = CreateMutex(NULL, FALSE, NULL);
    online_clients_mutex = CreateMutex(NULL, FALSE, NULL);
    
    // Khởi tạo danh sách online clients
    for (int i = 0; i < MAX_CLIENTS; i++) {
        online_clients[i].socket = INVALID_SOCKET;
    }
    
    // Đọc tài khoản
    load_accounts();

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

    printf("Login Server is running on port %d\n", port);

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
