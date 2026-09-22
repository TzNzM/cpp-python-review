1. 可迭代对象（iterable）和迭代器（iterator）分别是什么？举各一个例子。
可迭代对象就是：可以被 for 循环逐个取出元素的对象。比如：list、tuple、str、dict、set
迭代器就是一个知道“当前取到哪里了”，并且可以通过 next() 一个一个取元素的对象。
例子：
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
2. iter(obj) 和 next(iterator) 分别做什么？
iter(obj)把一个可迭代对象转换成迭代器
next(iterator) 从迭代器中取出下一个元素。
3. 迭代器没有元素可取时，next() 会发生什么？
会抛出：StopIteration
4. yield 与普通函数的 return 在执行行为上有什么区别？
return会直接结束函数，并把一个结果返回出去。
yield会产生一个值，然后暂停函数；下一次继续执行时，从上次暂停的位置继续。
def test():
    print("开始")
    yield 10
    print("继续")
    yield 20
    print("结束")

调用：

g = test()

注意：

这时候函数里面的代码还没有真正执行。

因为它是一个生成器。

第一次：

print(next(g))

执行过程：

开始
↓
yield 10
↓
暂停

输出：

开始
10

然后再：

print(next(g))

它不会从头开始，而是：

从 yield 10 后面继续
↓
print("继续")
↓
yield 20
↓
暂停

输出：

继续
20

再调用：

next(g)

继续：

print("结束")
↓
函数执行完毕
↓
StopIteration
5. 为什么生成器适合数据加载？为什么它又不能完全替代 PyTorch 的 DataLoader？
因为大量数据一次性加载到内存中，会使内存爆炸，所以需要生成器来加载。
生成器可以“一次加载一个”（惰性计算（Lazy Evaluation）数据真正需要的时候才生成。）

例如：

def load_data(filenames):
    for filename in filenames:
        image = load_image(filename)
        yield image

然后：

data_generator = load_data(filenames)

for image in data_generator:
    train(image)


因为 DataLoader 不只是简单地“一个一个产生数据”。

例如：

from torch.utils.data import DataLoader

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4
)

它可以帮你处理很多数据加载任务。
1.batch可以把数据直接组织成：
[x1, x2, ..., x32]

然后交给模型。
2.Shuffle可以把每个epoch的训练数据打乱
3.num_workers可以多进程加载数据
4.Dataset 与索引机制

PyTorch 通常把数据组织成：

class MyDataset(Dataset):
    def __len__(self):
        ...

    def __getitem__(self, index):
        ...

例如：

class MyDataset(Dataset):

    def __len__(self):
        return 10000

    def __getitem__(self, index):
        image = load_image(index)
        label = load_label(index)

        return image, label

然后：

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True
)

DataLoader 就可以根据 Dataset 的接口组织数据。

6. 生成器保存迭代进度；遍历到末尾后会耗尽，不能复用。训练的每个 epoch 应重新创建生成器，或使用可重复迭代的数据加载对象。