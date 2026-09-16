#include<exception>
#include<iostream>

// 1. 第一个：复制构造函数
// Resource(const Resource&) = delete;

// 它对应的是：

// Resource a;

// Resource b = a;    // ❌ 禁止

// 或者：

// Resource b(a);     // ❌ 禁止

// 这里发生的事情是：

// 已经存在一个对象 a
//        ↓
// 用 a 创建一个全新的对象 b
//        ↓
// 需要调用复制构造函数

// 也就是：

// Resource b(a);
//         ↓
// Resource(const Resource&)

// 所以：

// Resource(const Resource&) = delete;

// 就是：

// 不允许通过另一个 Resource 对象来创建新的 Resource 对象。

// 2. 第二个：复制赋值运算符
// Resource& operator=(const Resource&) = delete;

// 它对应的是：

// Resource a;
// Resource b;

// b = a;    // ❌ 禁止

// 注意这里和上面的区别。

// 此时：

// a：已经存在
// b：也已经存在

// a
// ↓
// 把 a 的内容复制给 b

// 调用的是：

// operator=

// 也就是：

// b = a;

// 实际上相当于：

// b.operator=(a);

// 所以：

// Resource& operator=(const Resource&) = delete;

// 表示：

// 不允许把一个已经存在的 Resource 复制赋值给另一个已经存在的 Resource。
class Resource
{
private:
    static int m_count;
public:
    Resource();
    ~Resource();
    
    //禁止复制构造、复制赋值
    Resource(const Resource&) = delete;
    Resource& operator=(const Resource&) = delete;

    //静态只读访问器
    static int count() noexcept { return m_count;}
};

Resource::Resource()
{
    ++m_count;
    std::cout << "创建，当前数量：" << m_count << '\n';
}

Resource::~Resource()
{
    --m_count;
    std::cout << "销毁，当前数量：" << m_count << '\n';
}

int Resource::m_count = 0; 

void process(bool shouldFail){
    Resource s1;
    Resource s2;
    if (shouldFail)
    {
        throw std::runtime_error("运行错误");
    }
}

int main(){
    process(false);
    std::cout << "正常路径后 count = " << Resource::count() << '\n';
    std::cout << "--------------" << std::endl;
    try
    {
        process(true);
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }
    std::cout << "异常路径后 count = " << Resource::count() << '\n';
}