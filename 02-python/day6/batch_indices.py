import random


def iter_batch_indices(n_samples, batch_size, shuffle=False, seed=None):
    if batch_size <= 0 or n_samples < 0:
        raise ValueError("数据输入有误")
    batch_list = list(range(0,n_samples,1))
    if shuffle:
        rand = random.Random(seed)
        rand.shuffle(batch_list)
    batch_total = []
    for i in range(0,n_samples,batch_size):
        batch = batch_list[i:i+batch_size]
        yield batch
    #     batch_total.append(batch)
    # return batch_total
def main():
    print(list(iter_batch_indices(10, 3,True))) # list(generator)会不断调用生成器的 next()。
    # [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]])

    # loader 是一次具体的生成器对象，不是可重复使用的数据容器。
    loader = iter_batch_indices(5, 2)

    first_epoch = list(loader)
    print(first_epoch)
    second_epoch = list(loader)
    print(second_epoch)

    # 这样才会两次都有数据
    # first_epoch = list(iter_batch_indices(5, 2))
    # second_epoch = list(iter_batch_indices(5, 2))
    #或者这样：每个循环都重新创建一个loader
    for epoch in range(2):
        loader = iter_batch_indices(5, 2)

        print(f"epoch {epoch}")
        for batch in loader:
            print(batch)


if __name__ == "__main__":
    main()