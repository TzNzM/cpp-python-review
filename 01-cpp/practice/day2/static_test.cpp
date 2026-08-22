#include<iostream>

int next_id(){
    static int id = 99;
    ++id;
    return id;
}

int main(){
    int id;
    id = next_id();
    std::cout << id << std::endl;
    id = next_id();
    std::cout << id << std::endl;
    id = next_id();
    std::cout << id << std::endl;
}