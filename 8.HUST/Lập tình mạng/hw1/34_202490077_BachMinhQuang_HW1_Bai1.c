#include <stdio.h>
#include <stdlib.h>

int my_strlen(char* s) {
    int len = 0;
    while (s[len] != '\0') {
        len++;
    }
    return len;
}

char* subStr(char* s1, int offset, int number) {
    // Kiểm tra tính hợp lệ
    if (s1 == NULL || offset < 0 || number <= 0) {
        return NULL;
    }
    
    int len = my_strlen(s1);
    if (offset >= len) {
        return NULL;
    }
    
    // Tính độ dài thực tế
    int actual_length;
    if (offset + number > len) {
        actual_length = len - offset;
    } else {
        actual_length = number;
    }
    
    // Cấp phát bộ nhớ động
    char* result = (char*)malloc((actual_length + 1) * sizeof(char));
    if (result == NULL) {
        return NULL;
    }
    
    // Copy ký tự
    for (int i = 0; i < actual_length; i++) {
        result[i] = s1[offset + i];
    }
    result[actual_length] = '\0';
    
    return result;
}

int main() {
    int offset, number;
    char str[81];
    
    printf("Nhap offset va number: ");
    scanf("%d %d", &offset, &number);
    getchar(); // Xóa ký tự newline
    
    printf("Nhap xau str: ");
    fgets(str, 81, stdin);
    
    // Xóa ký tự newline nếu có
    int len = my_strlen(str);
    if (str[len - 1] == '\n') {
        str[len - 1] = '\0';
    }
    
    char* sub = subStr(str, offset, number);
    if (sub != NULL) {
        printf("-%s-\n", sub);
        free(sub);
    } else {
        printf("Invalid input\n");
    }
    
    return 0;
}
