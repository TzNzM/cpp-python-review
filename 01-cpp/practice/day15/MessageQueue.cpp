#include<queue>
#include<mutex>
#include<iostream>
#include <condition_variable>
#include <thread>
#include <functional>

class MessageQueue
{
private:
    std::mutex m_mtx;
    std::queue<int> m_queue;
    std::condition_variable m_cv_not_empty;
    std::condition_variable m_cv_not_full;
    const size_t m_max_size = 5;
    bool m_close = false;
public:
    MessageQueue(/* args */);
    ~MessageQueue();
    void push(int value);
    bool pop(int& value);
    void close();
    
};

MessageQueue::MessageQueue(/* args */)
{
}

MessageQueue::~MessageQueue()
{
}

//生产者调用
void MessageQueue::push(int value){
    std::unique_lock<std::mutex> lock(m_mtx);
    m_cv_not_full.wait(lock,[this](){
        return this->m_close || this->m_queue.size() < this->m_max_size;
    });

    if (m_close) {
        return;
    }

    m_queue.push(value);
    lock.unlock();
    m_cv_not_empty.notify_one();
}

//消费者调用
bool MessageQueue::pop(int& value){
    std::unique_lock<std::mutex> lock(m_mtx);
    m_cv_not_empty.wait(lock,[this](){
        return !this->m_queue.empty() || this->m_close;
    });

    if (m_queue.empty() && m_close) {
        return false;
    }

    value = m_queue.front();
    m_queue.pop();
    lock.unlock();
    m_cv_not_full.notify_one(); 
    return true;
}

void MessageQueue::close(){
    {
        std::lock_guard<std::mutex> lock(m_mtx);
        m_close = true;
    }
    m_cv_not_empty.notify_all();
    m_cv_not_full.notify_all();
}

void producer(MessageQueue& mq){
    for (int i = 1; i <= 20; i++)
    {
        mq.push(i);
    }
    mq.close();
}

void consumer(MessageQueue& mq){
    int value = 0;
    int results = 0;
    while (mq.pop(value))
    {
        results += value;
    }
    std::cout << results << std::endl;
}

int main(){
    MessageQueue mq;
    //std::ref(mq) 就是告诉 thread：别拷贝，给我引用
    //如果不用 std::ref 会怎么样？

    // 比如：

    // std::thread t1(producer, mq);

    // 你可以把它理解成：

    // 主线程：
    //     mq
    //      │
    //      │ 拷贝
    //      ↓
    // 线程内部：
    //     mq的副本

    // 那么就不是你想要的：

    // t1 ─────→ mq
    // t2 ─────→ mq

    // 而可能变成：

    // t1 ─────→ mq副本1

    // t2 ─────→ mq副本2

    // 这当然不符合生产者消费者模型。

    // 更关键的是，如果 MessageQueue 包含：

    // std::mutex
    // std::condition_variable

    // 这个类本身通常就不可复制，因此直接传：

    // mq

    // 会导致编译错误。
    std::thread t1(producer, std::ref(mq));
    std::thread t2(consumer, std::ref(mq));

    t1.join();
    t2.join();
}
