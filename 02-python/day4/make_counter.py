def make_counter(start=0):
    count = start
    def counter():
        nonlocal count
        count += 1 # 关键：让内部函数能"写"外层的 count
        return count
    return counter

x = 100  # 全局变量 x

def shadow_demo():
    x = 1  # 局部变量，与全局 x 同名，在函数内部"遮蔽"了全局 x
    print("函数内部 x =", x)  # 读到的是局部 x

def main():
    counter_a = make_counter(10)
    print(counter_a())  # 11
    print(counter_a())  # 12

    counter_b = make_counter()
    print(counter_b())  # 1
    print(counter_a())  # 13

    shadow_demo()                      # 打印 1
    print("函数外部 x =", x)           # 打印 100，全局 x 没被改
    print("两个 x 是不是同一个对象:", "不是 —— 局部 x 遮蔽(shadowing)了全局 x")

if __name__ == "__main__":
    main()