#include <stdio.h>
#include <string.h>

void vulnerable_function(char* input) {
    char buffer[10];
    strcpy(buffer, input);  // 缓冲区溢出漏洞
}

int main() {
    char input[20] = "AAAAAAAAAAAAAAAAAAAA";  // 20个A，超过buffer大小
    vulnerable_function(input);
    return 0;
}