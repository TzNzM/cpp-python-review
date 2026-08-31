#include<iostream>
#include<string>
#include<stack>

bool is_valid_brackets(const std::string& text){
    std::stack<char> s;
    for (auto it = text.cbegin(); it != text.cend(); it++)
    {
        if (*it == '(' || *it == '[' || *it == '{')
        {
            s.push(*it);
        }else if (*it == ')')
        {
            if (s.empty())
            {
                return false;
            }            
            if (s.top() == '(')
            {
                s.pop();
                continue;
            }else
            {
                return false;
            }
        }else if (*it == ']')
        {
           
            if (s.empty())
            {
                return false;
            }
            if (s.top() == '[')
            {
                s.pop();
                continue;
            }else
            {
                return false;
            }
        }else if (*it == '}')
        {
            if (s.empty())
            {
                return false;
            }            
            if (s.top() == '{')
            {
                s.pop();
                continue;
            }else
            {
                return false;
            }
        }else
        {
            continue;
        }
    }
    if (s.empty())
    {
        return true;
    }else
    {
        return false;
    }
}

int main(){
    // std::string text = "(([abc])){}";
    // std::string text = "(([abc])){";
    std::string text = "]";
    std::cout << is_valid_brackets(text);
}