#include<list>
#include<iostream>

void remove_even(std::list<int>& values){
    // 空 vector 的特殊情况
    if (values.empty())
    {
        return;
    }
    for (auto it = values.begin(); it != values.end(); )
    {
        if (*it % 2 == 0)
        {
            it = values.erase(it);
        }else{
            ++it;
        }
        
    }
    
}

int main(){
    // std::list<int> values = {1,4,4,7,8,9,22};
    std::list<int> values = {};
    remove_even(values);
    for (auto it = values.begin(); it != values.end(); ++it)
    {
        std::cout << *it << std::endl;
    }
}