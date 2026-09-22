

def make_square_list(n):
    square_list = []
    for i in range(n):
        square_list.append(i**2)
    return square_list

def make_square_generator(n):
    return (i ** 2 for i in range(n)) #这个就是生成器表达式

def main():
    list = make_square_list(5)
    print(list)
    print(list)
    g = make_square_generator(5)
    print(next(g))
    print(next(g))

    try:
        iteration = iter([10,20])
        print(next(iteration))
        print(next(iteration))
        print(next(iteration))
    except StopIteration:
        print("iteration stop")

if __name__ == "__main__":
    main()