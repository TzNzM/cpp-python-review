1、vector 和原生数组有什么区别？
原生数组：
- 长度通常固定；
- 不提供 size、erase、push_back 等成员函数；
- 需要自己管理边界。

vector：
- 连续存储；
- 自动管理内存；
- 可以动态增长；
- 有 size、capacity、erase、push_back 等接口；
- 扩容时可能导致指针、引用和迭代器失效。
2、size() 和 capacity() 有什么区别？
size() 表示当前实际元素数量；
capacity() 表示当前已分配的存储空间可以容纳多少个元素。
3、reserve() 和 resize() 有什么区别？
reserve(n) -> 预留容量，不创建新元素
resize(n)  -> 修改元素数量，可能创建或删除元素
4、std::string 可以通过下标访问字符吗？字符串下标从几开始？
可以，0