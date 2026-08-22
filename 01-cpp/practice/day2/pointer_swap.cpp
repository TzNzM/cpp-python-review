#include<iostream>

void swap_if_greater(int* a, int* b){
    if(a == nullptr || b == nullptr){
        return;
    }

    if (*a > *b)
    {
        int temp = *a;
        *a = *b;
        *b = temp;
    }
    
}

int main(){
    int a = 4,b = 3;
    swap_if_greater(&a,&b);
    std::cout << "a:" << a << ",b:" << b << std::endl;
}