#include<stdio.h>

typedef struct s_Program Program;
typedef struct s_ClassName ClassName;
typedef struct s_ClassName2 ClassName2;

struct s_Program {
    char* pv_variableWithAssign;
    bool pr_variable;
    int (*pv_testFunc)(Program *self);
};
 struct s_ClassName {
    char* pv_attr1;
    int attr2;
    ClassName* (*__init__)(ClassName *self, char* param1, int param2);
};
 struct s_ClassName2 {
    char* pv_attr1;
    int attr2;
    ClassName* (*__init__)(ClassName2 *self, char* param1, int param2);
};
 

int staticVarWithAssign = 123;

int staticVar;


char* staticTestFunc(int parameter) {
printf("%s\n", parameter);
return parameter.toString();
}

int Program_pv_testFunc(Program *self) {
int ternaryOperatorResult = 12 == 12 ? 1 : 2;
return 123;
}

ClassName* ClassName___init__(ClassName *self, char* param1, int param2) {

}

ClassName* ClassName2___init__(ClassName2 *self, char* param1, int param2) {

}



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
Classname* obj = new__Classname("sdkdjg" , 7685943);
Classname** objArr = new Classname [ 5 ];
return 0;
}
