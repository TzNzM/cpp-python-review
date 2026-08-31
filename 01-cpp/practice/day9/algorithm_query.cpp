#include<iostream>
#include<vector>
#include<algorithm>


bool contains_score(
    const std::vector<int>& scores,
    int target
){
    if (std::find(scores.cbegin(),scores.cend(),target) != scores.end())
    {
        return true;
    }else
    {
        return false;
    }
    
    
}

std::size_t count_score(
    const std::vector<int>& scores,
    int target
){
    return std::count(scores.cbegin(),scores.cend(),target);
}

std::size_t count_invalid_score(
    const std::vector<int>& scores
){
    return std::count_if(scores.cbegin(),scores.cend(),[](int score){
        return score < 0 || score > 100;
    });
}

bool has_perfect_score(
    const std::vector<int>& scores
){
    if (std::find_if(scores.cbegin(),scores.cend(),[](int score){
        return score == 100;
    }) != scores.end())
    {
        return true;
    }else
    {
        return false;
    }
}

int main(){
    std::vector<int> scores = {95,80,-1,80,105,100};
    std::cout << contains_score(scores,80) << std::endl; 
    std::cout << contains_score(scores,60) << std::endl; 
    std::cout << count_score(scores,80) << std::endl; 
    std::cout << count_invalid_score(scores) << std::endl; 
    std::cout << has_perfect_score(scores) << std::endl; 
}