#include<iostream>

//const int scores[] 实际上是const int* scores，即数组在传入函数参数时会退化为一个指针
void analyze_scores(
    const int scores[],
    int n,
    int& sum,
    int& max_score,
    int& passed_count
){
    if (n == 0)
    {
        return;
    }
    for (int i = 0; i < n; i++)
    {
        sum += scores[i];
        if (scores[i] > max_score)
        {
            max_score = scores[i];
        }
        if (scores[i] >= 60)
        {
            passed_count++;
        }
    }  
}

int main(){
    const int scores[] = {59, 60, 100, 0, 60};
    int n = 5,sum = 0,max_score = 0,passed_count = 0;
    analyze_scores(scores,n,sum,max_score,passed_count);
    std::cout << sum << std::endl;
    std::cout << max_score << std::endl;
    std::cout << passed_count << std::endl;
}