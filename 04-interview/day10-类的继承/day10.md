回忆部分：
1.public 继承表达的是什么关系？
class Student : public Person 表达“Student 是一种 Person”，即 is-a 关系。
在访问权限上，Person 的 public 成员在 Student 中仍是 public，protected 成员仍是 protected；private 成员仍不能被派生类直接访问。
2.private、protected、public 成员分别能被谁访问？
private只能被其自身访问
protected能被其自身和其派生类访问
public能被其自身、其派生类和外部调用访问
3.构造一个派生类对象时，基类和派生类的构造顺序是什么？
先构造基类部分，再构造派生类自己的成员，最后执行派生类构造函数体。
4.析构顺序又是什么？
像栈一样的顺序，先创建的最后析构，
5.为什么基类的私有成员不会直接“消失”，但派生类不能直接访问它？
派生类对象内部包含完整的基类子对象，因此 Person 的 name 仍然存在，也会在构造 Person 时完成初始化。
private 限制的是访问权限，不是成员是否存在；所以 Student 不能直接写 name，但可通过 Person 提供的公开成员函数读取它。
面试题：
1.class Student : public Person 中的 public 有什么含义？若改成 private 继承会怎样？
public 表示公开继承，语义是“Student 是 Person”。外部代码可以把 Student 当作 Person 使用，例如调用继承来的公开成员函数。
若改成 private 继承，Person 原本的 public 和 protected 成员会成为 Student 的私有成员，对外部代码不可见；但 Student 自己的成员函数仍能访问它们。Person 原本的 private 成员始终不能直接访问。
2.为什么 Student 的初始化列表中应写 Person(name, age)，而不是先在构造函数体中处理？
因为进入 Student 构造函数体之前，Person 基类部分就必须已经构造完成。
初始化列表是在构造基类；构造函数体中只能执行普通语句，不能重新调用基类构造函数。若 Person 没有默认构造函数，就必须在初始化列表中传入 name 和 age。
3.protected 与 private 的区别是什么？为什么不要轻易把成员设为 protected？
private只能被其自身访问
protected能被其自身和其派生类访问
不要轻易使用 protected 数据成员，因为派生类可直接修改它，可能破坏基类的数据约束；同时基类内部表示会被派生类依赖，之后重构基类更困难。通常优先把数据保持为 private，按需要提供成员函数。
4.派生类能否直接访问基类的 private name？应该怎样安全读取它？
不能，应由 Person 提供公开的只读接口，例如 getName() const，Student 通过这个接口读取姓名。外部代码也可以通过 Student 对象调用该继承而来的公开接口。
5.创建和销毁 Student 对象时，构造/析构函数调用顺序分别是什么？为什么这样设计？
构造函数先创建person，然后student
析构函数先析构student，然后person
原因是 Student 依赖已构造完成的 Person 基类部分；析构时先清理派生类资源，清理期间基类仍然有效。