1、map 和 unordered_map 的底层结构及平均查找复杂度分别是什么？
map 通常基于平衡二叉搜索树，元素按 key 有序，查找、插入、删除通常为 O(log n)。

unordered_map 基于哈希表，元素无序，平均查找、插入、删除为 O(1)，
哈希冲突严重时最坏可能退化为 O(n)。
平均查找复杂度都是O（1）
2、m[key] 访问不存在的 key 会发生什么？
如果 key 不存在，operator[] 会创建这个 key，
并将 value 初始化为 mapped_type 的默认值，然后返回该 value 的引用。
3、find()、count()、at() 在访问不存在 key 时有什么区别？
find(key):
    找到 -> 返回指向元素的迭代器
    找不到 -> 返回 end()
    不会创建新 key

count(key):
    找到 -> 1
    找不到 -> 0
    不会创建新 key

at(key):
    找到 -> 返回 value 的引用
    找不到 -> 抛出 std::out_of_range
    不会创建新 key
4、insert() 插入重复 key 时会怎样？
插入新 key -> 插入成功
插入已存在的 key -> 插入失败，原来的 value 保持不变
5、为什么 map 的键不能通过迭代器修改？
map 的元素类型类似于：

std::pair<const Key, T>

key 被设计为 const，不能通过迭代器修改。
因为 map 依赖 key 维护有序结构；如果 key 被随意修改，
元素可能出现在错误的位置，破坏树的排序性质。

unordered_map 也不能直接修改 key，因为修改 key 后可能需要重新计算哈希值，
并且元素可能应该被放到另一个桶中，从而破坏哈希表结构。