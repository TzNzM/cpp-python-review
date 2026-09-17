
1. 位置参数与关键字参数的区别？
位置参数按顺序绑定；关键字参数按参数名绑定。关键字参数可提高可读性，也能避免位置写错。

1. 先看一个函数
def student(name, age, score):
    print(name, age, score)

调用：

student("Tom", 20, 90)

这里的：

"Tom"    → name
20       → age
90       → score

是按照位置对应的。

所以 "Tom" 是第 1 个参数 → name
20 是第 2 个参数 → age
90 是第 3 个参数 → score

这就是位置参数（positional argument）。

2. 关键字参数

你也可以明确写出参数名：

student(name="Tom", age=20, score=90)

这里不是靠第几个，而是靠：

name="Tom"
age=20
score=90

来对应。

这就是关键字参数（keyword argument）。

3. 两者可以混合

例如：

student("Tom", age=20, score=90)

这里：

"Tom"       # 位置参数
age=20      # 关键字参数
score=90    # 关键字参数

这是合法的。

但是有一个规则：

位置参数必须放在关键字参数前面。

比如：

student("Tom", age=20, score=90)   # ✅

但是：

student(name="Tom", 20, 90)        # ❌

因为位置参数 20、90 放到了关键字参数后面。

4. 为什么叫“位置”参数？

看这个函数：

def test(a, b, c):
    print(a, b, c)

调用：

test(10, 20, 30)

Python 实际上可以理解成：

第1个 → a
第2个 → b
第3个 → c

所以：

test(10, 20, 30)

和：

test(a=10, b=20, c=30)

在这个例子里效果一样。

5. 关键字参数的一个重要优点

关键字参数可以改变顺序：

def student(name, age, score):
    print(name, age, score)

可以：

student(score=90, name="Tom", age=20)

依然完全正确。

因为 Python 看的是参数名：

score → 90
name  → "Tom"
age   → 20

而位置参数就不行：

student(90, "Tom", 20)

这会变成：

name  = 90
age   = "Tom"
score = 20

虽然语法没错，但参数对应错了。
2. 默认参数是在函数定义时还是调用时创建？
在定义时创建的
3. 为什么 def f(items=[]) 可能有问题？
Python 的默认参数只会在 def 执行的时候创建一次，而不会每次调用函数都重新创建。
问题不在于“默认值为空”，而在于默认 list 是可变对象，多个未传该参数的调用会共享同一个 list。

先看这个有问题的代码
def f(items=[]):
    items.append(1)
    print(items)

f()
f()
f()

很多刚学 Python 的人会以为输出：

[1]
[1]
[1]

但实际上是：

[1]
[1, 1]
[1, 1, 1]
正确的写法是什么？

通常写成：

def f(items=None):
    if items is None:
        items = []

    items.append(1)
    print(items)
4. 函数返回多个值时，Python 实际返回的是什么？
返回的是一个tuple
5. 参数传递时，修改传入的 list 与给参数重新赋值，分别会不会影响调用方？
原地修改传入的 list 会影响调用方，因为双方引用同一个对象；给形参重新赋值只改变函数内部绑定，不影响调用方。
def test(lst):
    print("进入函数：", lst)

    lst.append(4)
    print("append之后：", lst)

    lst = [10, 20]
    print("重新赋值之后：", lst)


numbers = [1, 2, 3]

test(numbers)

print("函数外：", numbers)

输出：

进入函数： [1, 2, 3]
append之后： [1, 2, 3, 4]
重新赋值之后： [10, 20]
函数外： [1, 2, 3, 4]



