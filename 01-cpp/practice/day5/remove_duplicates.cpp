#include<vector>
#include<iostream>

void remove_duplicates(std::vector<int>& values){
    // 空 vector 的特殊情况
    if (values.empty())
    {
        return;
    }
    int temp;
    for (auto it = values.begin(); it != values.end(); )
    {
        if (it == values.begin())
        {
            temp = *it;
            ++it;
        }else
        {
            if (*it == temp)
            {
                it = values.erase(it);
            }else if (*it != temp)
            {
                temp = *it;
                ++it;
            }
        }
    }
}

int main(){
    std::vector<int> values = {1,1,2,2,2,3,5};
    // std::vector<int> values = {1,3};
    // std::vector<int> values;
    remove_duplicates(values);
    for (int i = 0; i < values.size(); i++)
    {
        std::cout << values.at(i) << std::endl;
    }
}