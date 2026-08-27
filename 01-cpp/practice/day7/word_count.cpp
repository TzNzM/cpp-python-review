#include <iostream>
#include <map>
#include <string>
#include <vector>

std::map<std::string, int> count_words(const std::vector<std::string>& words)
{
    std::map<std::string, int> results;

    for (auto it = words.cbegin(); it != words.cend(); ++it)
    {
        // operator[] 在 key 不存在时会创建它，并把 int 初始化为 0。
        // 因此这里可以直接递增，不需要先 count() 再 insert()。
        ++results[*it];
    }

    return results;
}

int main()
{
    std::vector<std::string> words = {"cpp", "python", "cpp", "map", "python", "cpp"};
    std::map<std::string, int> results = count_words(words);

    // map 遍历时会按照 key 的升序输出。
    for (auto it = results.cbegin(); it != results.cend(); ++it)
    {
        std::cout << it->first << ": " << it->second << std::endl;
    }
}

// -------------------- 旧代码：保留但注释掉 --------------------
// #include<iostream>
// #include<vector>
// #include<map>
//
// std::map<std::string, int> count_words(const std::vector<std::string>& words){
//     std::map<std::string, int> results;
//     for (auto it = words.cbegin(); it != words.cend(); it++)
//     {
//         if (results.count(*it))
//         {
//             results[*it] += 1;
//         }else
//         {
//             results.insert({*it,1});
//         }
//     }
//     return results;
// }
//
// int main(){
//     std::vector<std::string> words = {"cpp", "python", "cpp", "map", "python", "cpp"};
//     std::map<std::string, int> results = count_words(words);
//     for (auto it = results.begin(); it != results.end(); it++)
//     {
//         std::cout << it->first << ":" << it->second << std::endl;
//     }
// }
