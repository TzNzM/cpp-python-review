#include<iostream>

void swap_if_greater(int& a, int& b){
    if ( a > b )
    {
        // int t = b;
        // b = a;
        // a = t;
        std::swap(a,b);
    }  
}

int main(){
    int a = 6;
    int b = 5;
    swap_if_greater(a,b);
    std::cout << "a:" << a << ",b:" << b << std::endl;
}