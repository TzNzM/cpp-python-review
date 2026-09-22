1. 列表、字典、集合推导式分别用什么括号？
列表 []
字典 {}
集合推导式 {}
2. [A if condition else B for x in xs] 和 [x for x in xs if condition] 的区别？
[A if condition else B for x in xs]：这是“二选一转换”：每个 x 都会保留，只是根据条件决定生成 A 或 B。
[x for x in xs if condition]：这是“过滤”：只有满足条件的 x 才会保留。
["偶数" if x % 2 == 0 else "奇数" for x in [1, 2, 3]]
# ["奇数", "偶数", "奇数"]

[x for x in [1, 2, 3] if x % 2 == 0]
# [2]
3. enumerate(items) 返回的两个值分别是什么？
它返回的是“索引和值”，即 (index, item)。

for index, item in enumerate(["cat", "dog"]):
    print(index, item)
# 0 cat
# 1 dog

4. zip(a, b) 在两者长度不同时会怎样？
它不会补 None，而是在较短序列结束时立刻停止，多余元素会被忽略：
list(zip([1, 2, 3], ["a", "b"]))
# [(1, "a"), (2, "b")]

5. sorted() 会修改原列表吗？any() 与 all() 分别在什么情况下为真？
sorted() 不修改原列表，而是返回一个新列表。会原地修改的是 list.sort()。
any(values)：至少一个元素为真，结果就是 True；空序列为 False。
all(values)：全部元素都为真，结果才是 True；空序列为 True。