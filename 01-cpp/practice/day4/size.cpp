#include<vector>
#include<iostream>

// size()     -> 当前有多少个元素
// capacity() -> 当前最多能容纳多少元素而不重新分配

// reserve(n) -> 改变容量，不改变元素数量
// resize(n)  -> 改变元素数量，必要时改变容量
int main(){
    std::vector<int> values;

    values.push_back(1);

    values.push_back(2);

    values.push_back(3);

    std::cout << values.size() << std::endl;
    std::cout << values.capacity() << std::endl;
    std::cout << "---------------" << std::endl;
    values.reserve(100);
    std::cout << values.size() << std::endl;
    std::cout << values.capacity() << std::endl;
    std::cout << "---------------" << std::endl;
    values.resize(5);
    std::cout << values.size() << std::endl;
    std::cout << values.capacity() << std::endl;
    std::cout << "---------------" << std::endl;
    values.resize(2);
    std::cout << values.size() << std::endl;
    std::cout << values.capacity() << std::endl;
    std::cout << "---------------" << std::endl;
}