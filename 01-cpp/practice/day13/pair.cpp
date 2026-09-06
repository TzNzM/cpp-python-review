// #include<iostream>

// template <typename T>
// class Pair
// {
// private:
//     T m_first;
//     T m_second;
// public:
//     Pair(T first,T second);
//     ~Pair();
//     T getFirst() const;
//     T getSecond() const;
//     void swap();
// };

// template <typename T>
// Pair<T>::Pair(T first,T second) : m_first(first),m_second(second)
// {
// }

// template <typename T>
// Pair<T>::~Pair()
// {
// }

// template <typename T>
// T Pair<T>::getFirst() const{
//     return m_first;
// }

// template <typename T>
// T Pair<T>::getSecond() const{
//     return m_second;
// }

// template <typename T>
// void Pair<T>::swap(){
//     std::swap(m_first,m_second);
// }

// int main(){
//     Pair<int> p(1,2);
//     std::cout << p.getFirst() << p.getSecond() << std::endl;
//     p.swap();
//     std::cout << p.getFirst() << p.getSecond() << std::endl;
//     Pair<double> p2(1.5,2.6);
//     std::cout << p2.getFirst() << p2.getSecond() << std::endl;
//     p2.swap();
//     std::cout << p2.getFirst() << p2.getSecond() << std::endl;
//     Pair<std::string> p3("right","left");
//     std::cout << p3.getFirst() << p3.getSecond() << std::endl;
//     p3.swap();
//     std::cout << p3.getFirst() << p3.getSecond() << std::endl;
// }

#include <iostream>
#include <string>
#include <utility>

template <typename T>
class Pair {
private:
    T m_first;
    T m_second;

public:
    Pair(const T& first, const T& second)
        : m_first(first), m_second(second) {
    }

    const T& getFirst() const {
        return m_first;
    }

    const T& getSecond() const {
        return m_second;
    }

    void swap() {
        using std::swap;
        swap(m_first, m_second);
    }
};

int main() {
    Pair<int> p1(1, 2);
    p1.swap();
    std::cout << p1.getFirst() << ' ' << p1.getSecond() << '\n';

    Pair<double> p2(1.5, 2.6);
    p2.swap();
    std::cout << p2.getFirst() << ' ' << p2.getSecond() << '\n';

    Pair<std::string> p3("right", "left");
    p3.swap();
    std::cout << p3.getFirst() << ' ' << p3.getSecond() << '\n';
}
