1.std::find 找不到元素时返回什么？
返回迭代器。

找到 -> 指向第一个匹配元素
找不到 -> 返回 end()
2.find_if 和 find 的区别是什么？
find     -> 查找等于指定值的元素
find_if  -> 查找满足条件的第一个元素
3.count 和 count_if 的区别是什么？
count     -> 统计等于指定值的元素数量
count_if  -> 统计满足条件的元素数量
4.remove_if 之后为什么还需要 erase？
它会：
1. 把不满足删除条件的元素移动到前面；
2. 返回新的逻辑结尾；
3. 但不改变容器的 size()。
因此需要：
new_end = remove_if(begin, end, condition)
erase(new_end, end)
这就是 erase-remove 惯用法。
5.std::sort 是否会改变原容器？
std::sort 会直接修改原容器指定范围内的元素，
按照默认规则或自定义规则重新排列。
6.std::transform 的常见用途是什么？
对范围内的每个元素执行某种变换，
并把结果写入目标范围。
7.accumulate 的初始值类型为什么重要？
初始值同时决定：
1. 累加从什么值开始；
2. 累加结果使用什么类型。
std::vector<double> values = {1.5, 2.5};

std::accumulate(values.begin(), values.end(), 0);   // 可能按 int 累加
std::accumulate(values.begin(), values.end(), 0.0); // 按 double 累加