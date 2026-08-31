#include<iostream>
#include<vector>
#include<algorithm>
#include <functional>

void remove_failed(
    std::vector<int>& scores,
    int pass_score
){
    auto new_end = std::remove_if(scores.begin(),scores.end(),[pass_score](int score){
        return score < pass_score;
    });
    scores.erase(new_end,scores.end());
}

void sort_descending(
    std::vector<int>& values
){
    std::sort(values.begin(),values.end(),[](int a, int b){
        return a > b;
    });
}

int main(){
    std::vector<int> scores = {59,90,45,60,76,30};
    remove_failed(scores,60);
    for (auto it = scores.cbegin(); it != scores.cend(); ++it)
    {
        std::cout << *it << std::endl;
    }
    sort_descending(scores);
    for (auto it = scores.cbegin(); it != scores.cend(); ++it)
    {
        std::cout << *it << std::endl;
    }

}