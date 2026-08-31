#include<vector>
#include<iostream>
#include<queue>
#include <algorithm>

std::vector<int> top_k_largest(
    const std::vector<int>& values,
    std::size_t k
){
    std::priority_queue<int,std::vector<int>,std::greater<int>> min_priority;
    std::vector<int> results;
    if (k == 0)
    {
        return results;
    }
    
    for (auto it = values.cbegin(); it != values.cend(); it++)
    {
        if (min_priority.size() < k)
        {
            min_priority.push(*it);
        }else if (min_priority.top() < *it)
        {
            min_priority.pop();
            min_priority.push(*it);
        }
    }

    results.resize(std::min(values.size(), k));
    int i = results.size()-1;
    while (!min_priority.empty())
    {
        results[i]=min_priority.top();
        min_priority.pop();
        --i;
    }


    // while (!min_priority.empty())
    // {
    //     results.push_back(min_priority.top());
    //     min_priority.pop();
    // }

    // std::reverse(results.begin(), results.end());
    
    return results;
    
}

int main(){
    std::vector<int> values = {3,1,8,2,5,9};
    std::size_t k = 100;
    std::vector<int> results = top_k_largest(values,k);
    for (auto it = results.cbegin(); it != results.cend(); ++it)
    {
        std::cout << *it << std::endl;
    }
}