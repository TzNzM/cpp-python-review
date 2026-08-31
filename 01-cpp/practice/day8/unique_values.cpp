#include<vector>
#include<set>
#include<unordered_set>
#include<iostream>

std::vector<int> unique_sorted(
    const std::vector<int>& values
){
    std::set<int> s;
    for (auto it = values.cbegin(); it != values.cend(); it++)
    {
        s.insert(*it);
    }
    std::vector<int> results;
    for (auto it = s.cbegin(); it != s.cend(); it++)
    {
        results.push_back(*it);
    }
    return results;
}

bool has_duplicate(
    const std::vector<int>& values
){
    std::unordered_set<int> s;
    for (auto it = values.cbegin(); it != values.cend(); it++)
    {
        if (s.count(*it))
        {
            return true;
        }else
        {
            s.insert(*it);            
        }
    }
    return false;
}

int main(){
    std::vector<int> values = {4,2,4,1,2,5};
    std::vector<int> results = unique_sorted(values);
    // unique_sorted 返回的结果已经按升序排列。
    for (auto it = results.cbegin(); it != results.cend(); ++it)
    {
        std::cout << *it << std::endl;
    }
    std::cout << has_duplicate(values) << std::endl;
}