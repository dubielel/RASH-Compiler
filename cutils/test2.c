#include <stdio.h>
int foo(int a, int b) {
    return a + b;
}

struct data
{
    int (*func)(int a, int b);
};

int main(void) {
    struct data a;
    a.func = foo;

    printf("%d", a.func(2, 3));
}