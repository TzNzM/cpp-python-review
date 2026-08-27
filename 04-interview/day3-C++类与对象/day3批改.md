# Day 3 批改与总结：C++ 类与对象

## 一、当前检查结果

### Rectangle

`Rectangle` 已基本正确：

- `private` 成员封装宽和高；
- 构造函数已使用初始化列表；
- `area()`、`perimeter()` 是 `const` 成员函数；
- `resize()` 会拒绝宽或高小于等于 0 的输入；
- `const Rectangle` 可以调用 `area()`。

当前程序编译运行成功，面积、周长和 resize 测试结果符合预期。

### BankAccount

正常存款和取款流程正确，`deposit(0)` 也已经被拒绝。

仍有一个边界问题：

```cpp
if (amount < 0 || amount > m_nbalance)
```

这会允许 `withdraw(0)` 返回 `true`。题目要求金额必须大于 0，因此应当拒绝 0。

还需要补测：

```text
deposit(0)    -> false
deposit(-10)  -> false
withdraw(0)   -> false
withdraw(-10) -> false
withdraw(200) -> false，余额不变
```

`BankAccount` 构造函数仍是在函数体中赋值，后续可以改用初始化列表。

### Tracker

运行顺序正确：

```text
construct:a
construct:b
construct:c
destroy:c
destroy:b
destroy:a
```

构造顺序是 `a -> b -> c`，析构顺序是 `c -> b -> a`。内层作用域先结束，后构造的对象先析构。

`Tracker` 构造函数也可以改为初始化列表。

## 二、面试问题检查

### `private` 和 `public`

回答正确。`private` 只能在类内部访问，`public` 可以在类内外访问。封装的意义是隐藏内部状态，通过公开接口控制修改规则。

### 初始化列表

标准答案：初始化列表在构造函数函数体执行前直接初始化成员变量，避免先默认初始化再赋值。对于 `const` 成员、引用成员和没有默认构造函数的成员，初始化列表是必须的。

### `const` 成员函数

`const` 成员函数承诺不会通过当前对象修改普通成员变量，因此可以被 `const` 对象调用，编译器也会检查函数内部是否修改对象状态。

```cpp
int area() const;
```

因为 `area()` 只读取宽和高，所以适合声明为 `const`。

### 普通局部对象和局部 static

普通局部对象离开作用域时析构；局部 `static` 第一次执行到声明时初始化，在程序结束时析构，作用域仍然只在当前函数内部。

## 三、今天的核心总结

```text
private       -> 隐藏内部状态
public        -> 暴露可使用的接口
初始化列表    -> 直接初始化成员
const 成员函数 -> 只读对象状态
析构函数       -> 对象生命周期结束时执行
```

今天的重点是：类通过封装保护状态，构造函数负责建立初始状态，`const` 成员函数表达只读接口，析构函数和作用域决定对象何时结束生命周期。

## 四、剩余问题

1. `withdraw(0)` 仍应拒绝；
2. `BankAccount` 和 `Tracker` 可以改用初始化列表；
3. 头文件可以增加 `#pragma once`；
4. 补充金额边界测试。

这些问题不影响类与对象主线概念的掌握，但属于代码完整性和工程习惯。