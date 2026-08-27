#include <iostream>
#include <string>
#include <unordered_map>

bool add_stock(
    std::unordered_map<std::string, int>& inventory,
    const std::string& item,
    int amount
)
{
    // find() 只查找一次，同时可以直接修改找到的元素。
    // 这样比 count() 后再使用 operator[] 少一次哈希查找。
    auto it = inventory.find(item);
    if (it == inventory.end())
    {
        return false;
    }

    it->second += amount;
    return true;
}

bool get_stock(
    const std::unordered_map<std::string, int>& inventory,
    const std::string& item,
    int& amount
)
{
    // const 容器不能使用 operator[]，因为 operator[] 可能创建新 key。
    // find() 有 const 版本，不会修改 inventory。
    auto it = inventory.find(item);
    if (it == inventory.end())
    {
        amount = 0;
        return false;
    }

    amount = it->second;
    return true;
}

int main()
{
    std::unordered_map<std::string, int> inventory = {{"apple", 10}, {"banana", 5}};

    std::cout << add_stock(inventory, "apple", 3) << std::endl;
    std::cout << add_stock(inventory, "orange", 4) << std::endl;

    int amount;
    std::cout << get_stock(inventory, "banana", amount) << std::endl;
    std::cout << amount << std::endl;
    std::cout << get_stock(inventory, "orange", amount) << std::endl;
    std::cout << amount << std::endl;
}

// -------------------- 旧代码：保留但注释掉 --------------------
// #include<unordered_map>
// #include<string>
// #include<iostream>
//
// bool add_stock(
//     std::unordered_map<std::string, int>& inventory,
//     const std::string& item,
//     int amount
// ){
//     if (inventory.count(item))
//     {
//         inventory[item] += amount;
//         return true;
//     }else
//     {
//         return false;
//     }
// }
//
// bool get_stock(
//     const std::unordered_map<std::string, int>& inventory,
//     const std::string& item,
//     int& amount
// ){
//     if (inventory.count(item))
//     {
//         amount = inventory.at(item); // 为啥不能用 inventory[item]
//         return true;
//     }else
//     {
//         amount = 0;
//         return false;
//     }
// }
//
// int main(){
//     std::unordered_map<std::string, int> inventory = {{"apple",10},{"banana",5}};
//     std::cout << add_stock(inventory,"apple",3) << std::endl;
//     std::cout << add_stock(inventory,"orange",4) << std::endl;
//     int amount;
//     std::cout << get_stock(inventory,"banana",amount) << std::endl;
//     std::cout << amount << std::endl;
//     std::cout << get_stock(inventory,"orange",amount) << std::endl;
//     std::cout << amount << std::endl;
// }
