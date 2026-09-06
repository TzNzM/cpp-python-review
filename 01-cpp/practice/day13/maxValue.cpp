#include<iostream>


template <typename T>
const T& maxValue(const T &a,const T &b){
    return a >= b ? a : b;
}

int main(){
    std::cout << maxValue(3,7) << std::endl;
    std::cout << maxValue(2.5,1.2) << std::endl;
    std::string s1 = "cat";
    std::string s2 = "dog";
    std::cout << maxValue(s1,s2) << std::endl;
    std::cout << maxValue<int>(3,7) << std::endl;
}