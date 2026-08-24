#include<iostream>
#include"Rectangle.h"
#include"BankCount.h"

int main(){
    //Rectangle test
    Rectangle rec = Rectangle(3,4);
    std::cout << rec.area() << std::endl;
    std::cout << rec.perimeter() << std::endl;
    int height = 5,width = 2;
    std::cout << rec.resize(height,width) << std::endl;
    height = -8;
    std::cout << rec.resize(height,width) << std::endl;

    const Rectangle rect(3, 4);
    std::cout << rect.area() << std::endl;

    //BankCountTest
    BankAccount bk("bob",100);
    bk.deposit(50);
    std::cout << bk.balance() << std::endl;
    bk.withdraw(50);
    std::cout << bk.balance() << std::endl;
    bk.withdraw(-10);
    std::cout << bk.balance() << std::endl;

    
}