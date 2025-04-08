
        #include <stdio.h>
        
        int add(int a, int b) {
            return a + b;
        }
        
        int multiply(int a, int b) {
            return a * b;
        }
        
        int main() {
            int x = 5;
            int y = 3;
            printf("Add: %d\n", add(x, y));
            printf("Multiply: %d\n", multiply(x, y));
            return 0;
        }
        