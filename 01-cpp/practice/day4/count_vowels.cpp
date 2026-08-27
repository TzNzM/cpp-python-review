#include<string>
#include<iostream>

int count_vowels(const std::string& text){
    int count = 0;
    // 推荐使用
    // for (char ch : text) {
    // // 检查 ch
    // }
    for (int i = 0; text.cbegin()+i < text.cend() ; ++i)
    {
        if (text.at(i) == 'a' || text.at(i) == 'e' || text.at(i) == 'i' || text.at(i) == 'o' || text.at(i) == 'u' ||
            text.at(i) == 'A' || text.at(i) == 'E' || text.at(i) == 'I' || text.at(i) == 'O' || text.at(i) == 'U')
        {
            ++count;
        }
        
    }
    return count;
    
}

int main(){
    std::string s = "Hello";
    std::cout << count_vowels(s) << std::endl;
}