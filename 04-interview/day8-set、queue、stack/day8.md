1、set 和 unordered_set 的底层结构、顺序特性和查找复杂度有什么区别？
set 通常基于平衡二叉搜索树，元素按 key 有序，
查找、插入、删除通常为 O(log n)。

unordered_set 基于哈希表，元素无序，
平均查找、插入、删除为 O(1)，最坏为 O(n)。
2、set 插入重复元素时会怎样？
插入重复元素时不会真的插入进去，而是保持原set不变
insert 通常返回 pair<iterator, bool>，
第二个成员表示是否插入成功。
3、queue、stack 分别遵循什么顺序？核心接口有哪些？
queue是队列，先进先出 front()、back()、push()、pop()、empty()、size()
stack是栈，先进后出，top()、push()、pop()、empty()、size()
4、为什么 queue 和 stack 通常不能使用 begin()、end()？
queue 和 stack 是容器适配器，
只暴露符合队列或栈语义的接口，
不提供通用迭代器，因此通常没有 begin() 和 end()。
5、priority_queue 默认是大顶堆还是小顶堆？top()、push()、pop() 的复杂度分别是什么？
priority_queue 默认是大顶堆。
top()是O(1)
push()是O(logn)
pop()是O(logn)
6、如何声明一个小顶堆？
std::priority_queue<
    int,
    std::vector<int>,
    std::greater<int>
> min_heap;