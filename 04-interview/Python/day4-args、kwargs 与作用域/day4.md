1. *args 在函数内部是什么类型？
tuple 类型
2. **kwargs 在函数内部是什么类型？
dict 类型
3. 为什么位置参数不能写在关键字参数之后？
Python 要求位置参数先完成按顺序绑定，再处理关键字参数，因此 f(a=1, 2) 直接违反参数语法规则；
4. LEGB 作用域查找顺序是什么？
Local     当前函数内部
Enclosing 外层函数
Global    当前 Python 文件
Built-in  Python 内置名称，例如 len、print
5. global 与 nonlocal 分别修改哪一层作用域的变量？
nonlocal 只用于修改最近一层外部函数变量；global 则用于修改整个 Python 文件中的全局变量。global 更准确地说是修改当前模块的全局绑定，不是整个项目所有文件的变量。