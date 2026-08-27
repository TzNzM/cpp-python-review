#include<iostream>
#include<string>

std::string reverse_copy(const std::string& text){
    std::string new_text;
    auto new_it = new_text.begin();
    for (auto it = text.rbegin(); it != text.rend(); )
    {
        new_it = new_text.insert(new_it,*it);
        ++it;
        ++new_it;
    }
    return new_text;
}

int main(){
    std::string s = "levela";
    std::string new_s = reverse_copy(s);
    std::cout << new_s << std::endl;
}