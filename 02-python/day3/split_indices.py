import random


def split_indices(n_samples, ratio=0.8, seed=42, shuffle=True):
    train = []
    val = []
    arr =  list(range(0,n_samples))
    if ratio >= 1.0 or ratio <= 0:
        raise ValueError("划分比例错误")
    if n_samples <= 0:
        raise ValueError("采样个数错误")
    if shuffle:
        rng = random.Random(seed)
        rng.shuffle(arr)
    train = arr[:(int)(n_samples*ratio)]
    val = arr[(int)(n_samples*ratio):]
    return train,val
def main():
    train,val = split_indices(10,ratio=0.78,shuffle=True)
    print(train)
    print(val)

if __name__ == "__main__":
    main()