#include<deque>
#include<iostream>

void append_with_limit(
    std::deque<int>& values,
    int value,
    std::size_t max_size
){
    if (max_size == 0)
    {
        while(!values.empty())
        {
            values.pop_front();
        }
        return;       
    }else if (max_size > values.size())
    {
        values.push_back(value);
        return;
    }else if (max_size == values.size())
    {
        values.pop_front();
        values.push_back(value);
        return;
    }
    
    while (max_size < values.size())
    {
        values.pop_front();
    }
    values.pop_front();
    values.push_back(value);
}

int main(){
    std::deque<int> values = {1,2,3,5};
    append_with_limit(values,4,2);
    for (auto it = values.begin(); it != values.end(); ++it)
    {
        std::cout << *it << std::endl;
    }
}
