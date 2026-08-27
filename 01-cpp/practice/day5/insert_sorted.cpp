#include<iostream>
#include<vector>

void insert_sorted(std::vector<int>& values, int value){
    
    // 空 vector 的特殊情况
    if (values.empty())
    {
        values.insert(values.begin(), value);
        return;
    }

    for (auto it = values.begin(); it != values.end(); )
    {
        if (*it >= value)
        {
            it = values.insert(it,value);
            return;
        }else{
            ++it;
            if (it == values.end())
            {
                it = values.insert(it,value);
                return;
            }
            
        }
    }
    
}

int main(){
    // std::vector<int> values;
    // std::vector<int> values = {1,3,5};
    std::vector<int> values = {1,3};
    int value = 4;
    insert_sorted(values,value);
    for (int i = 0; i < values.size(); i++)
    {
        std::cout << values.at(i) << std::endl;
    }
}