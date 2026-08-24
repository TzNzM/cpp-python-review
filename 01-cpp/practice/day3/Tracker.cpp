#include<string>
#include<iostream>
// 对象按照创建顺序构造；
// 离开作用域时析构；
// 析构顺序与构造顺序相反；
// 内层作用域的对象先析构。
class Tracker {

    private:
        std::string m_sname;
    public:
        Tracker(const std::string& name);
        ~Tracker();
};

Tracker::Tracker(const std::string& name){
    m_sname = name;
    std::cout << "construct:" << name << std::endl;
}

Tracker::~Tracker(){
    std::cout << "destroy:" << m_sname << std::endl;
}

int main(){
    Tracker a("a");

    {
        Tracker b("b");
        Tracker c("c");
    }
}