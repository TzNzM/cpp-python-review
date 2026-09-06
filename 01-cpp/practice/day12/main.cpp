#include <iostream>
#include <string>
#include <vector>
#include <memory>

class Person
{
private:
    std::string m_sname;
protected:
    int m_nage;
public:
    Person(std::string name,int age);
    virtual ~Person() = default;
    std::string getName() const;
    int getAge() const;
    virtual void introduce() const = 0;
};

Person::Person(std::string name,int age) : m_sname(name),m_nage(age)
{
    std::cout << "Person constructed:" << m_sname << std::endl;
}

std::string Person::getName() const{
    return m_sname;
}

int Person::getAge() const{
    return m_nage;
}

// void Person::introduce() const{
//     std::cout << "Name" << this->getName() << std::endl;
//     std::cout << "Age:" << this->m_nage << std::endl;
// }

//为什么 virtual 不能让它“不需要定义”？

// virtual 表示的是：

// 这个函数支持动态绑定。
// Person::~Person()
// {
// }


class Student : public Person
{
private:
    std::string m_sstudentID;
public:
    Student(std::string name,int age,std::string studentID);
    ~Student();
    void birthday();
    void introduce() const override;
};

Student::Student(std::string name,int age,std::string studentID) : Person(name,age),m_sstudentID(studentID)
{
    std::cout << "Student constructed:" << m_sstudentID << std::endl;
}

Student::~Student()
{
    std::cout << "Student delete:" << std::endl;
}

void Student::birthday(){
    this->m_nage += 1;
}

void Student::introduce() const{
    std::cout << "ID:" << this->m_sstudentID << std::endl;
    std::cout << "Name" << this->getName() << std::endl;
    std::cout << "Age:" << this->m_nage << std::endl;
}

class Teacher : public Person
{
private:
    std::string m_ssubject;
public:
    Teacher(std::string name,int age,std::string m_ssubject);
    ~Teacher();
    void birthday();
    void introduce() const override;
};

Teacher::Teacher(std::string name,int age,std::string subject) : Person(name,age),m_ssubject(subject)
{
    std::cout << "Teacher constructed:" << m_ssubject << std::endl;
}

Teacher::~Teacher()
{
    std::cout << "Teacher delete:" << std::endl;
}

void Teacher::birthday(){
    this->m_nage += 1;
}


void Teacher::introduce() const{
    std::cout << "Subject:" << this->m_ssubject << std::endl;
    std::cout << "Name" << this->getName() << std::endl;
    std::cout << "Age:" << this->m_nage << std::endl;
}


int main(){
    std::vector<std::unique_ptr<Person>> people;
    people.push_back(std::make_unique<Student>("Bob", 25, "S1001"));
    people.push_back(std::make_unique<Teacher>("Bob", 25, "Science"));
    for (size_t i = 0; i < people.size(); i++)
    {
        people[i]->introduce();
    }
}
