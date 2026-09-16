#include<iostream>
#include<thread>
#include<mutex>
#include<condition_variable>
#include<queue>
#include<future>

// promise 和 future 本质上是一对“线程之间共享结果的通信工具”。

// promise 是结果的生产者/写入端，future 是结果的消费者/读取端。

// 它们背后通常会共享一块由标准库管理的 shared state（共享状态）。

//                     共享状态
//                  ┌─────────────┐
//                  │             │
// promise ────────>│   int = ?   │<────── future
//   写入            │             │        读取
//                  │   状态：未就绪 │
//                  └─────────────┘

class MessageQueue
{
private:
    size_t m_max_size = 5;
    std::mutex m_mtx;
    std::queue<int> m_queue;
    std::condition_variable m_cv_not_empty;
    std::condition_variable m_cv_not_full;
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

void MessageQueue::push(int value){
    std::unique_lock<std::mutex> lock(m_mtx);
    m_cv_not_full.wait(lock,[this](){
        return m_queue.size() < m_max_size && !m_close;
    });

    m_queue.push(value);
    m_cv_not_empty.notify_one();
}

bool MessageQueue::pop(int& value){
    std::unique_lock<std::mutex> lock(m_mtx);
    m_cv_not_empty.wait(lock,[this](){
        return !m_queue.empty() || m_close;
    });

    if (m_queue.empty() && m_close)
    {
        return false;
    }

    value = m_queue.front();
    m_queue.pop();
    m_cv_not_full.notify_one();
    return true;
}

void MessageQueue::close(){
    {
        std::unique_lock<std::mutex> lock(m_mtx);
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

void consumer(MessageQueue& mq,std::promise<int> promise){
    int value = 0;
    int results = 0;
    while (mq.pop(value))
    {
        results += value;
    }
    promise.set_value(results);
}

int main(){
    MessageQueue mq;
    std::promise<int> t2_promise; //我承诺以后会给你一个 int 类型的结果
    std::promise<int> t3_promise;
    std::future<int> t2_future = t2_promise.get_future(); //我将来可以从这里拿到一个 int
    std::future<int> t3_future = t3_promise.get_future();
    std::thread t1(producer,std::ref(mq));
    std::thread t2(consumer,std::ref(mq),std::move(t2_promise)); //std::move(t2_promise) 把 promise 移动到了子线程。
    std::thread t3(consumer,std::ref(mq),std::move(t3_promise));

    int results_t2 = t2_future.get();
    int results_t3 = t3_future.get();
    std::cout << results_t2 << std::endl;
    std::cout << results_t3 << std::endl;

    t1.join();
    t2.join();
    t3.join();
}

//std::async 内部帮你把这套东西(promise 和 future)封装起来了。
// #include <iostream>
// #include <future>

// int add(int a, int b)
// {
//     return a + b;
// }

// int main()
// {
//     std::future<int> result = std::async(std::launch::async, add, 10, 20);

//     std::cout << "主线程继续执行..." << std::endl;

//     int value = result.get();

//     std::cout << "线程返回值：" << value << std::endl;

//     return 0;
// }
