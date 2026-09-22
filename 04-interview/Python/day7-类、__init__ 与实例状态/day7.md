1. 类与实例分别是什么？
类是对象的“蓝图”或类型定义，描述对象应有哪些数据和行为；实例是根据这个类创建出的具体对象。
2. self 指向什么？为什么实例方法必须写它？
dog_a.name = "A"
dog_b.name = "B"
当执行 dog_a.show_name() 时，方法里的 self 就是 dog_a；执行 dog_b.show_name() 时，self 就是 dog_b。因此同一个方法能读取、修改各自实例的数据。
类本身通常通过类名访问，例如 Dog.species；在类方法中则常用 cls 表示类。
3. __init__ 在什么时候调用？
当通过类创建实例、执行 类名(...) 时，Python 会自动调用 __init__ 初始化这个新对象。
4. 类属性与实例属性的存储和共享方式有什么区别？
类属性定义在类体中，默认由所有实例共享：
class Dog:
    species = "canine"
实例属性通常在 __init__ 中通过 self.xxx 创建，每个实例各自保存：
def __init__(self, name):
    self.name = name
修改 Dog.species 会影响没有同名实例属性的所有实例；但执行 dog_a.species = "custom" 会在 dog_a 上创建同名实例属性，遮蔽类属性，不影响其他实例。
5. 为什么多数情况下优先用组合，而不是为了复用而随意继承？
组合是“对象内部持有另一个对象”，表达清晰的“has-a”关系；继承表达的是“is-a”关系。
例如，Trainer 拥有一个 MetricTracker，适合组合；Dog 是 Animal 的一种，才可能适合继承。为了复用几行代码就继承，会让子类强依赖父类内部设计，耦合更高、修改更危险，也容易形成不合理的类型关系。


MindMap：
Python 面向对象
│
├── 类与对象
│   ├── class
│   ├── object
│   ├── self
│   └── __init__
│
├── 封装
│   ├── _xxx
│   ├── __xxx
│   └── @property
│
├── 继承
│   ├── class A(B)
│   ├── super()
│   ├── 方法重写
│   ├── 多继承
│   └── MRO
│
├── 多态
│   ├── 方法重写
│   └── 鸭子类型
│
├── 抽象与接口
│   ├── ABC
│   ├── @abstractmethod
│   └── Protocol
│
├── 组合
│   └── has-a
│
├── 方法
│   ├── 实例方法
│   ├── @classmethod
│   └── @staticmethod
│
└── 特殊方法
    ├── __str__
    ├── __eq__
    ├── __add__
    ├── __len__
    ├── __iter__
    └── ...

## Python的类的一些知识总结：
1. Python 的“私有成员”

Python 和 C++ 不太一样。

C++：

private:
    int money;

Python 通常使用：

self._money

表示：

这是内部使用的成员，外部最好不要直接访问。

还有：

self.__money

双下划线会触发 name mangling（名称改写）。

例如：

class Account:
    def __init__(self):
        self.__money = 100

Python 会把它内部改写成类似：

_Account__money

所以：

account.__money

通常访问不到。

不过需要注意：

Python 的封装更多依赖约定，而不是像 C++ 那样严格的 private 访问控制。

2. 继承的写法
class Unit:
    def move(self):
        print("移动")


class Zealot(Unit):
    def attack(self):
        print("近战攻击")


class Stalker(Unit):
    def attack(self):
        print("远程攻击")
3. 多态
因为 Python 更关注：

这个对象有没有 speak()？

而不是：

这个对象是不是 Animal 的子类？

例如：

class Dog:
    def speak(self):
        print("汪汪")


class Cat:
    def speak(self):
        print("喵喵")

现在：

animals = [
    Dog(),
    Cat()
]

for animal in animals:
    animal.speak()

输出：

汪汪
喵喵

注意这里：

animal.speak()

我们根本不关心 animal 到底是：

Dog

还是：

Cat

只要它具有：

speak()

就可以。

4. 方法重写
继承以后，子类可以重新定义父类的方法。

class Animal:
    def speak(self):
        print("动物发出声音")


class Dog(Animal):
    def speak(self):
        print("汪汪")

5. super() 是干什么的
class Animal:
    def __init__(self, name):
        self.name = name


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

这里：

super().__init__(name)

就是调用父类的：

Animal.__init__(name)

于是：

dog = Dog("旺财", "金毛")

最终对象拥有：

dog
├── name = "旺财"
└── breed = "金毛"

6. 多继承
class Flyable:
    def fly(self):
        print("飞行")


class Swimmable:
    def swim(self):
        print("游泳")


class Duck(Flyable, Swimmable):
    pass

duck = Duck()

duck.fly()
duck.swim()

7. MRO

MRO：

Method Resolution Order

也就是方法解析顺序。

例如：

class A:
    def test(self):
        print("A")


class B(A):
    def test(self):
        print("B")


class C(A):
    def test(self):
        print("C")


class D(B, C):
    pass

执行：

d = D()
d.test()

输出：

B

可以查看：

print(D.mro())

大致会得到：

D
B
C
A
object

Python 会按照这个顺序寻找方法。

8. 组合（has a）
组合的思想是：

一个对象里面包含另一个对象。

例如：

class Engine:
    def start(self):
        print("发动机启动")


class Car:
    def __init__(self):
        self.engine = Engine()

    def start(self):
        self.engine.start()
        print("汽车启动")

9. 为什么很多时候推荐组合而不是继承？

假设：

class Animal:
    def move(self):
        pass

然后你不断：

Animal
├── Dog
├── Cat
├── Bird
├── Fish
├── ...

如果行为越来越复杂，继承树可能变成：

Animal
├── FlyingAnimal
│   ├── Eagle
│   └── Sparrow
├── SwimmingAnimal
│   ├── Fish
│   └── Duck
└── ...

很容易变得复杂。

组合则可以把能力拆开：

class FlyBehavior:
    def fly(self):
        print("飞行")


class SwimBehavior:
    def swim(self):
        print("游泳")

然后：

class Duck:
    def __init__(self):
        self.fly_behavior = FlyBehavior()
        self.swim_behavior = SwimBehavior()

这样可以自由组合能力。

这背后的工程思想叫：

Composition over Inheritance

优先使用组合，而不是过度使用继承。

10. 抽象接口的写法

### 第一种写法：ABC 抽象基类
from abc import ABC, abstractmethod

所有具体子类都必须提供 speak() 的实现。
class Animal(ABC):

    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        print("汪汪")

### 第二种写法：Protocol
from typing import Protocol


class Animal(Protocol):

    def speak(self):
        ...
class Dog:
    def speak(self):
        print("汪汪")
注意这里的Dog没有继承自Animal，但是从接口的角度来看，Dog 依然符合 Animal 这个 Protocol。因为它有：Speak函数

### 第三种写法：纯粹的鸭子类型
啥都不需要，只是相同的函数名字
class Dog:
    def speak(self):
        print("汪汪")


class Cat:
    def speak(self):
        print("喵喵")


def make_sound(animal):
    animal.speak()
11. 属性Property

class Person:
    def __init__(self, age):
        self._age = age

    @property
    def age(self):
        return self._age
使用时（看起来像访问变量，实际上是在调用age()函数）：
person = Person(20)

print(person.age)

当然还可以设置setter
class Person:
    def __init__(self, age):
        self._age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("年龄不能为负数")
        self._age = value
用属性语法隐藏方法调用。
使用时：
person.age = 25

12. 实例方法、类方法、静态方法
实例方法：（self表示当前对象）
class Student:
    def hello(self):
        print(self)
类方法：（cls表示当前类）
class Student:

    count = 0

    @classmethod
    def get_count(cls):
        return cls.count
静态方法：
class Math:

    @staticmethod
    def add(a, b):
        return a + b
他的适用方法就是 Math.add(1,2)

13. 特殊方法/魔术方法
魔术方法就是 Python 预先规定好的一组特殊方法。它们通常以 __xxx__ 的形式命名，用来让你的对象参与 Python 语言本身的各种操作。
魔术方法
│
├── 对象创建/初始化
│   ├── __new__
│   └── __init__
│
├── 对象表示
│   ├── __str__
│   └── __repr__
│
├── 比较
│   ├── __eq__
│   ├── __lt__
│   ├── __le__
│   ├── __gt__
│   └── __ge__
│
├── 算术运算
│   ├── __add__
│   ├── __sub__
│   ├── __mul__
│   └── __truediv__
│
├── 容器行为
│   ├── __len__
│   ├── __getitem__
│   ├── __setitem__
│   ├── __contains__
│   └── __iter__
│
├── 上下文管理
│   ├── __enter__
│   └── __exit__
│
└── 属性访问
    ├── __getattr__
    ├── __getattribute__
    └── __setattr__

| 你写的代码           | Python 背后调用              |
| --------------- | ------------------------ |
| `obj = Class()` | `__new__` → `__init__`   |
| `print(obj)`    | `__str__`                |
| `repr(obj)`     | `__repr__`               |
| `a == b`        | `__eq__`                 |
| `a < b`         | `__lt__`                 |
| `a + b`         | `__add__`                |
| `len(obj)`      | `__len__`                |
| `obj[i]`        | `__getitem__`            |
| `obj[i] = x`    | `__setitem__`            |
| `x in obj`      | `__contains__`           |
| `iter(obj)`     | `__iter__`               |
| `next(obj)`     | `__next__`               |
| `obj()`         | `__call__`               |
| `with obj:`     | `__enter__` / `__exit__` |
| `obj.attr`      | `__getattribute__`       |
| 找不到 `obj.attr`  | `__getattr__`            |
| `obj.attr = x`  | `__setattr__`            |

14. 最后四种关系回顾
第一组：继承
Dog → Animal

回答：

Dog 是一种 Animal。

关键词：

is-a
第二组：组合
Car → Engine

回答：

Car 拥有一个 Engine。

关键词：

has-a
第三组：多态
for obj in objects:
    obj.run()

回答：

不同对象可以通过统一的接口表现出不同的行为。

第四组：接口/抽象
class Worker(ABC):
    @abstractmethod
    def work(self):
        pass

回答：

规定对象必须提供哪些行为，而不规定具体实现。
