#include<vector>
#include<iostream>
#include<string>
#include<queue>

std::vector<std::string> serve_customers(
    const std::vector<std::string>& customers,
    std::size_t count
){
    std::queue<std::string> q;
    std::vector<std::string> results;
    for (auto it = customers.cbegin(); it != customers.cend(); it++)
    {
        q.push(*it);
    }
    for (size_t i = 0; i < count && !q.empty(); i++)
    {
       results.push_back(q.front());
       q.pop();
    }
    return results;
}

int main(){
    std::vector<std::string> customers = {"Alice","Bob","Carol"};
    size_t count = 2;
    std::vector<std::string> results =  serve_customers(customers,count);
    for (auto it = results.cbegin(); it != results.cend(); ++it)
    {
        std::cout << *it << std::endl;
    }
}