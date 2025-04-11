void vulnerable_function() {
    char buffer[10];
    printf("Enter some text: ");
    gets(buffer);  // 使用 gets 可能导致缓冲区溢出
    printf("You entered: %s\n", buffer);
}