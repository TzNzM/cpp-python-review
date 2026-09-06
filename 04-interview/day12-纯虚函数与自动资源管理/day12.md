1.虚函数与纯虚函数的区别是什么？
虚函数使用 virtual 声明，基类可以提供默认实现；通过基类指针或引用调用时，会根据对象的动态类型选择实际执行的派生类版本。
纯虚函数写作 virtual void f() = 0;，它使类成为抽象类。非抽象派生类必须重写该函数。纯虚函数通常不提供实现，但语法上也可以有函数体；其中纯虚析构函数必须提供函数体。
2.为什么包含纯虚函数的类不能直接创建对象？抽象类能否有成员变量、构造函数和普通成员函数？
因为这个类有未实现的函数，实际上这个类就是抽象类。都可以有
3.为什么可以用 std::unique_ptr<Person> 管理 Student、Teacher 对象？
Student 和 Teacher 都公开继承自 Person，因此派生类对象可以通过 Person* 使用。unique_ptr<Person> 独占拥有这个对象，并只暴露 Person 的接口。
4.已经使用 unique_ptr<Person> 后，为什么 Person 仍应有虚析构函数？
unique_ptr<Person> 默认销毁对象时，本质上仍会通过 Person* 执行 delete。只有 Person 的析构函数是虚函数，删除时才会先调用实际派生类（如 Student）的析构函数，再调用 Person 的析构函数。
如果基类析构函数不是虚函数，却通过 Person* 删除派生类对象，行为是未定义的，可能导致派生类资源没有被正确释放。
5.“面向接口编程”在这个例子中具体体现在哪里？
那个introduce就是一个接口，容器只认识 Person，调用统一的 introduce()；它不需要判断对象到底是 Student 还是 Teacher。