1.为什么线程结束前需要 join()？销毁一个仍可 join 的 std::thread 会怎样？
join() 会阻塞当前线程，直到目标线程执行结束，并回收该线程的执行资源。这样可以保证后续代码使用线程结果前，目标线程已经完成。
如果 std::thread 对象析构时仍处于 joinable 状态，程序会调用 std::terminate()，通常会直接异常终止。线程对象离开作用域前必须 join() 或 detach()。
2.什么是数据竞争？为什么 counter++ 在多线程中不是天然安全的？
数据竞争是多个线程在没有同步的情况下并发访问同一内存位置，且至少有一个访问是写操作。数据竞争会导致未定义行为。
counter++ 不是单一步骤，而是“读取 counter、加一、写回 counter”。两个线程可能同时读到相同旧值，分别加一后写回，导致其中一次更新丢失。
3.std::lock_guard 与 std::unique_lock 分别适合什么场景？
std::lock_guard 适合简单的作用域加锁：构造时加锁，离开作用域自动解锁，期间不能手动解锁或重新加锁。
std::unique_lock 更灵活，支持延迟加锁、手动 lock()/unlock() 和所有权转移；std::condition_variable::wait() 需要使用 unique_lock，因为等待时必须临时释放锁并在被唤醒后重新加锁。
4.为什么条件变量应使用 wait(lock, predicate)，而不是只写 wait(lock)？
条件变量可能发生伪唤醒：线程即使没有收到与条件对应的通知，也可能从 wait() 返回。只写 wait(lock) 后若直接继续执行，可能在队列为空时错误地取数据。
wait(lock, predicate) 会在锁保护下反复检查谓词；谓词为 false 时才等待，唤醒后会再次检查。它等价于用 while 循环包裹 wait(lock)，可以正确处理伪唤醒和多个线程竞争同一份数据。
5.notify_one() 与 notify_all() 有什么区别？为什么 close() 通常需要 notify_all()？
notify_one() 唤醒一个等待在该条件变量上的线程；notify_all() 唤醒所有等待线程。被唤醒的线程仍需重新竞争 mutex 并检查谓词。
close() 表示不会再有新数据。可能有多个消费者正在等待“队列非空”，它们都需要醒来并发现“队列已关闭且为空”，然后退出；因此通常使用 notify_all()。若有生产者因队列满而等待，关闭时也应唤醒它们。
