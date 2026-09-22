1. 子类继承父类时，super() 的作用是什么？
super() 不只是“调用父类”，而是按 MRO 查找父类实现；
2. @property 为什么能在不改变 obj.label 使用方式的前提下加入校验？
@property 把方法包装成属性访问。读取 record.label 时会自动调用 getter，赋值 record.label = value 时会自动调用 setter；调用方仍使用普通属性语法，而类内部可以完成校验、清洗和拒绝非法值。
3. __repr__ 与 __str__ 分别面向什么场景？
__repr__打印的东西是面向程序员的
__str__打印的东西是面向用户的
4. __len__、__getitem__、__iter__ 能分别让对象支持什么 Python 操作？
__len__能让调用len()函数，__getitem__能让对象支持像List一样按索引下标访问，__iter__ 使对象支持 iter(batch) 和 for；直接调用 next() 需要的是迭代器，例如 next(iter(batch))。
5. __eq__ 默认比较什么？自行实现后通常应比较什么？
默认的 __eq__ 是对象身份比较；自定义时应比较“业务上决定两个对象是否相等”的字段，例如 path、label、prediction，不一定机械比较所有属性。

子类重写 __init__ 会覆盖父类的初始化过程。漏掉 super().__init__(path) 时，父类负责创建的 self.path 不存在，因此访问 record.path 会报 AttributeError。
