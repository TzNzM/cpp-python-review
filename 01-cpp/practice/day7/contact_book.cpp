#include <iostream>
#include <map>
#include <string>

bool add_contact(
    std::map<std::string, std::string>& contacts,
    const std::string& name,
    const std::string& phone
)
{
    // emplace() 直接尝试插入，并通过 second 表示是否插入成功。
    // key 已存在时不会覆盖原来的电话号码。
    auto result = contacts.emplace(name, phone);
    return result.second;
}

bool find_contact(
    const std::map<std::string, std::string>& contacts,
    const std::string& name,
    std::string& phone
)
{
    // find() 只查找一次；找到后通过迭代器读取 value。
    auto it = contacts.find(name);
    if (it == contacts.end()) //如果没找到就会返回迭代器的end
    {
        return false;
    }

    phone = it->second;
    return true;
}

int main()
{
    std::map<std::string, std::string> contacts;
    add_contact(contacts, "Alice", "111");
    add_contact(contacts, "Bob", "222");

    bool judge = add_contact(contacts, "Alice", "999");
    std::cout << judge << std::endl;

    std::string phone;
    if (find_contact(contacts, "Alice", phone))
    {
        std::cout << phone << std::endl;
    }
    else
    {
        std::cout << "not found" << std::endl;
    }

    // map 默认按 key 升序遍历，因此这里会按姓名顺序打印。
    for (auto it = contacts.cbegin(); it != contacts.cend(); ++it)
    {
        std::cout << it->first << ": " << it->second << std::endl;
    }

    // 查询失败时不使用 phone，因为它可能仍然保存上一次查询的旧值。
    if (find_contact(contacts, "Carol", phone))
    {
        std::cout << phone << std::endl;
    }
    else
    {
        std::cout << "Carol: not found" << std::endl;
    }
}

// -------------------- 旧代码：保留但注释掉 --------------------
// #include<map>
// #include<iostream>
//
// bool add_contact(
//     std::map<std::string, std::string>& contacts,
//     const std::string& name,
//     const std::string& phone
// ){
//     if (contacts.count(name))
//     {
//         return false;
//     }else{
//         contacts.insert({name,phone});
//         return true;
//     }
// }
//
// bool find_contact(
//     const std::map<std::string, std::string>& contacts,
//     const std::string& name,
//     std::string& phone
// ){
//     if (!contacts.count(name))
//     {
//         return false;
//     }else{
//         phone = contacts.at(name);
//         return true;
//     }
// }
//
// int main(){
//     std::map<std::string, std::string> contacts;
//     add_contact(contacts,"Alice","111");
//     add_contact(contacts,"Bob","222");
//     bool judge = add_contact(contacts,"Alice","999");
//     std::cout << judge << std::endl;
//     std::string phone;
//     std::cout << find_contact(contacts,"Alice",phone) << std::endl;
//     std::cout << phone << std::endl;
//     std::cout << find_contact(contacts,"Carol",phone) << std::endl;
//     std::cout << phone << std::endl;
//
//     // 没明白怎么按顺序打印？
// }
