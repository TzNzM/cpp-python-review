#include<iostream>
#include<vector>
#include<numeric>
#include<algorithm>

std::vector<int> double_values(
    const std::vector<int>& values
){
    std::vector<int> results;
    results.resize(values.size());
    std::transform(values.begin(),values.end(),results.begin(),[](int value)->int{
        return value * 2;
    });
    return results;
}

int sum_values(
    const std::vector<int>& values
){
    return std::accumulate(values.begin(),values.end(),0);
}

int main(){
    std::vector<int> value = {1,2,3,4};
    std::vector<int> results = double_values(value);
    for (auto it = results.cbegin(); it != results.cend(); ++it)
    {
        std::cout << *it << std::endl;
    }
    std::cout << sum_values(value) << std::endl;
}