#include<iostream>
int sum_positive(const int* values, int n){
    int sum = 0;
    if (values == nullptr)
    {
        return sum;
    }
    
    for (int i = 0; i < n; i++)
    {
        if (*(values+i) <= 0)
        {
            continue;
        }else
        {
            sum += *(values+i);
        }       
    }
    return sum;    
}

int main(){
    const int values[] = {3,-2,5,0,-7};
    int n = 5;
    int sum;
    sum = sum_positive(values,n);
    std::cout << sum << std::endl;
}