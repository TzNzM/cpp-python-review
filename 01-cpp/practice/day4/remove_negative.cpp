#include<vector>
#include<iostream>

void remove_negatives(std::vector<int>& values){
    for (auto it = values.begin(); it != values.end();)
    {
        if (*it < 0)
        {
            it = values.erase(it); //erase删除当前元素之后，会让元素向左移动
        }else{
            ++it;
        }
        
    }
    
}

int main(){
    std::vector<int> values = {1,-2,3,-4,5};
    remove_negatives(values);
    for (int i = 0; i < values.size(); i++)
    {
        std::cout << values.at(i) << std::endl;
    }
    
}