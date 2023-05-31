#include "../cutils/methods_map.h"

#include<stdio.h>

typedef struct s_Program Program;
typedef struct s_ClassName ClassName;
typedef struct s_ClassName2 ClassName2;

struct s_Program {
    METHODS_MAP* methods;
    char* pv_variableWithAssign;
    bool pr_variable;
};
 struct s_ClassName {
    METHODS_MAP* methods;
    char* pv_attr1;
    int attr2;
};
 struct s_ClassName2 {
    METHODS_MAP* methods;
    char* pv_attr1;
    int attr2;
};
 

int staticVarWithAssign = 123;

int staticVar;


char* staticTestFunc(int parameter) {
printf("%s\n", parameter);
return parameter.toString();
}

void* Program_pv_testFunc(void** args) {
Program* self = *((Program**) args[0]);

int ternaryOperatorResult = 12 == 12 ? 1 : 2;
return (void)* & 123;
}

Program* new__Program(void** args, int args_count) {
    Program* obj = (Program*) malloc(sizeof(Program);
    obj.methods = init_methods_map(3);
    insert_methods_map(obj.methods, "testFunc", Program_pv_testFunc);
    return obj;}

void* ClassName___init__(void** args) {
ClassName* self = *((ClassName**) args[0]);
char* param1 = *((char**) args[1]);
int param2 = *((int*) args[2]);


}

ClassName* new__ClassName(void** args, int args_count) {
    ClassName* obj = (ClassName*) malloc(sizeof(ClassName);
    obj.methods = init_methods_map(1);
    insert_methods_map(obj.methods, "__init__", ClassName___init__);
    return obj;}

void* ClassName2___init__(void** args) {
ClassName2* self = *((ClassName2**) args[0]);
char* param1 = *((char**) args[1]);
int param2 = *((int*) args[2]);


}

ClassName2* new__ClassName2(void** args, int args_count) {
    ClassName2* obj = (ClassName2*) malloc(sizeof(ClassName2);
    obj.methods = init_methods_map(1);
    insert_methods_map(obj.methods, "__init__", ClassName2___init__);
    return obj;}



int main(int argc, char** args) {
int x = 0;
while (x < 100) {
x += 1;
if (x % 3 == 0 && x % 5 == 0) {
printf("%s\n", "FizzBuzz");
} else if (x % 3 == 0) {
printf("%s\n", "Fizz");
} else if (x % 5 == 0) {
printf("%s\n", "Buzz");
} else {
printf("%d\n", x);
}
}
return 0;
}