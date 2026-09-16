#include<iostream>
#include<exception>
#include<string>
#include<algorithm>
#include<cctype>
#include<limits>


double divide(int a,int b){
    if (b == 0){
        throw std::invalid_argument("除数不能为0");
    }
    return static_cast<double> (a) / b;
}

int parsePositiveInt(const std::string& text){
    int num = 0;
    if (text.empty())
    {
        throw std::invalid_argument("数值为空");
    }
    if (*(text.cbegin()) == '-' || text == "0")
    {
        throw std::domain_error("数值小于等于0");
    }
    for (auto it = text.cbegin(); it != text.cend(); it++)
    {      
        if (std::isdigit(*it))
        {
            int value = static_cast<int> (*it - '0');
            if (num > (std::numeric_limits<int>::max() - value) / 10)
            {
                throw std::out_of_range("超出int范围");
            }else
            {
                num = 10*num + value;
            }
        }else
        {
            throw std::invalid_argument("输入不是数字");
        }  
    }
    return num;
}

int main(){
    try
    {
        double result = divide(10,0);
        std::cout << result << std::endl;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }
    
    try
    {
        double result = divide(10,3);
        std::cout << result << std::endl;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }

    try
    {
        std::string s ="1234";
        std::cout << parsePositiveInt(s) << std::endl;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }

    try
    {
        std::string s ="123dasdas=";
        std::cout << parsePositiveInt(s) << std::endl;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }

    try
    {
        std::string s ="89461884848451684654897";
        std::cout << parsePositiveInt(s) << std::endl;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }

    try
    {
        std::string s ="-89461884848451684654897";
        std::cout << parsePositiveInt(s) << std::endl;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }
    
}