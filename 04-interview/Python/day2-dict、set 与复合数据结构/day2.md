1. dict[key] 与 dict.get(key) 在 key 不存在时分别怎样？
dict[key] 访问不存在的会报错，而 dict.get(key) 会返回None
2. 字典的 key 为什么通常必须是不可变、可哈希对象？
key 必须是“可哈希的”，因为字典依赖 hash 定位；其 hash 值在作为 key 的期间必须稳定。通常选不可变对象，如 str、int、元素也可哈希的 tuple。
3. set 为什么适合做去重和集合比较？
set 同时支持平均 O(1) 的成员查询，以及交、并、差等集合运算；它是无序容器。
4. 如何只记录某个标签第一次出现的下标？
set 只能记住“是否见过”，不能保存第一次出现的下标。应使用 dict：当标签首次出现时，写入 first_indices[label] = i。可先判断 label not in first_indices。
5. list 和 set 的成员查找复杂度通常分别是多少？
set 通常/平均为 O(1)，极端哈希冲突时可能退化为 O(n)。

dict的用法：
| 操作       | 用法               | 作用                    |
| -------- | ---------------- | --------------------- |
| 创建       | `d = {}`         | 创建空字典                 |
| 获取       | `d[key]`         | 获取 value              |
| 获取       | `d.get(key)`     | 获取 value，不存在返回 `None` |
| 添加       | `d[key] = value` | 添加键值对                 |
| 修改       | `d[key] = value` | 修改 value              |
| 删除       | `del d[key]`     | 删除                    |
| 删除       | `d.pop(key)`     | 删除并返回 value           |
| 判断       | `key in d`       | 判断 key 是否存在           |
| 所有 key   | `d.keys()`       | 获取所有 key              |
| 所有 value | `d.values()`     | 获取所有 value            |
| 键值对      | `d.items()`      | 获取 key-value 对        |
| 批量更新     | `d.update(...)`  | 更新多个键值对               |
| 清空       | `d.clear()`      | 清空字典                  |
| 长度       | `len(d)`         | 键值对数量                 |
set的用法：
| 操作  | 写法             | 作用        |
| --- | -------------- | --------- |
| 创建  | `set()`        | 空集合       |
| 创建  | `{1, 2, 3}`    | 集合        |
| 添加  | `s.add(x)`     | 添加元素      |
| 删除  | `s.remove(x)`  | 删除，不存在报错  |
| 删除  | `s.discard(x)` | 删除，不存在不报错 |
| 判断  | `x in s`       | 是否存在      |
| 长度  | `len(s)`       | 元素个数      |
| 清空  | `s.clear()`    | 清空        |
| 交集  | `a & b`        | 共同元素      |
| 并集  | `a \| b`       | 所有元素      |
| 差集  | `a - b`        | a 有、b 没有  |
| 对称差 | `a ^ b`        | 只属于其中一个   |
| 去重  | `set(list)`    | list 去重   |


d.pop(key) 在 key 不存在时也会抛 KeyError；可传默认值避免异常。
set 的元素同样必须可哈希，例如不能把 list 直接加入 set。
set(list) 去重后不保证保留原始顺序；若业务需要保持首次出现顺序，不能只依赖 set