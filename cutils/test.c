#include <stdio.h>
#include "methods_map.h"

int foo(int a, int b) {
    return a + b;
}

void* addIntegers(void** args) {
    int a = *((int*) args[0]);
    int b = *((int*) args[1]);
    int sum = a + b;
    printf("Sum of %d and %d is: %d\n", a, b, sum);
    return (void*) &sum;
}

int main(void) {
    printf("p");
    METHODS_MAP* methods_map = init_methods_map(1);
    printf("p");
    insert_methods_map(methods_map, "addIntegers", addIntegers);
    printf("p");

    printf("%d", *((int*) call_method_methods_map(methods_map, "addIntegers")((void*)((void*[2]){&(int){1}, &(int){2}}))));

    delete_methods_map(methods_map);
}