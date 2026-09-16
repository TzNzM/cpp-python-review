#include<mutex>
#include<iostream>
#include<thread>

class SafeCounter
{
private:
    int m_count;
    mutable std::mutex m_mtx;
public:
    SafeCounter();
    ~SafeCounter();
    void increment();
    int value() const;
};

SafeCounter::SafeCounter()
{
    m_count = 0;
}

void SafeCounter::increment()
{
    // m_mtx.lock();
    // m_count++;
    // m_mtx.unlock();
    std::lock_guard<std::mutex> lock(m_mtx);

    m_count++;
}

int SafeCounter::value() const
{
    std::lock_guard<std::mutex> lock(m_mtx);
    return m_count;
}

SafeCounter::~SafeCounter()
{
}

int main(){
    SafeCounter s;
    std::thread t1([&s](){
        for (int i = 0; i < 10000; i++)
        {
            s.increment();
        }  
    });
    std::thread t2([&s](){
        for (int i = 0; i < 10000; i++)
        {
            s.increment();
        }  
    });
    std::thread t3([&s](){
        for (int i = 0; i < 10000; i++)
        {
            s.increment();
        }  
    });
    std::thread t4([&s](){
        for (int i = 0; i < 10000; i++)
        {
            s.increment();
        }  
    });
    
    t1.join();
    t2.join();
    t3.join();
    t4.join();

    std::cout << s.value() << std::endl;

}
