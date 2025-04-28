#include <stdio.h>
#include <string.h>

void vulnerable_function(char* input) {
    char buffer[10];
    // 缓冲区溢出漏洞
    strcpy(buffer, input);  
}

int main() {
    char input[20] = "AAAAAAAAAAAAAAAAAAAA";  
    vulnerable_function(input);
    return 0;
}





