#include <iostream>
#include <string>

class Person
{
private:
    std::string m_sname;
protected:
    int m_nage;
public:
    Person(std::string name,int age);
    ~Person();
    std::string getName() const;
    int getAge() const;
};

Person::Person(std::string name,int age) : m_sname(name),m_nage(age)
{
    std::cout << "Person constructed:" << m_sname << std::endl;
}

Person::~Person()
{
}

std::string Person::getName() const{
    return m_sname;
}

int Person::getAge() const{
    return m_nage;
}


class Student : public Person
{
private:
    std::string m_sstudentID;
public:
    Student(std::string name,int age,std::string studentID);
    ~Student();
    void birthday();
    void introduce() const;
};

Student::Student(std::string name,int age,std::string studentID) : Person(name,age),m_sstudentID(studentID)
{
    std::cout << "Student constructed:" << m_sstudentID << std::endl;
}

Student::~Student()
{
}

void Student::birthday(){
    this->m_nage += 1;
}

void Student::introduce() const{
    std::cout << "ID:" << this->m_sstudentID << std::endl;
    std::cout << "Name" << this->getName() << std::endl;
    std::cout << "Age:" << this->m_nage << std::endl;
}


int main(){
    Student s("Alice", 20, "S1001");
    s.introduce();
    s.birthday();
    s.introduce();
}
