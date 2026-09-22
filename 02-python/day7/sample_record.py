from cProfile import label

from numpy import empty
from sympy import false


class SampleRecord:
    def __init__(self, path, label, prediction=None):
        if isinstance(path,str) and path is not None and path != "":
            self._path = path.strip()
        else:
            raise TypeError("类型不正确或为空")
        if isinstance(label,str) and label != "":
            self._label = label
        else:
            raise TypeError("类型不正确或为空")
        if isinstance(prediction,str) or prediction is None:
            self._prediction = prediction
        else:
            raise TypeError("类型不正确")

    def is_correct(self):
        if self._prediction is None:
            return None
        else:
            if self._label == self._prediction:
                return True
            else:
                return False

def main():
    # 1. 合法样本
    print("测试1：合法样本")
    sample = SampleRecord(
        " data/cat_001.jpg ",
        "cat"
    )

    print(sample._path)
    print(sample._label)
    print(sample._prediction)
    print()


    # 2. 预测正确
    print("测试2：预测正确")
    sample = SampleRecord(
        "data/cat_001.jpg",
        "cat",
        "cat"
    )

    print(sample.is_correct())
    assert sample.is_correct() is True
    print("测试通过")
    print()


    # 3. 预测错误
    print("测试3：预测错误")
    sample = SampleRecord(
        "data/cat_001.jpg",
        "cat",
        "dog"
    )

    print(sample.is_correct())
    assert sample.is_correct() is False
    print("测试通过")
    print()


    # 4. 空路径
    print("测试4：空路径")
    try:
        SampleRecord(
            "",
            "cat"
        )
        print("测试失败：应该抛出异常")
    except TypeError as e:
        print("测试通过：", e)
    print()


    # 5. 空标签
    print("测试5：空标签")
    try:
        SampleRecord(
            "data/cat_001.jpg",
            ""
        )
        print("测试失败：应该抛出异常")
    except TypeError as e:
        print("测试通过：", e)
    print()


    # 6. 非法预测
    print("测试6：非法预测")
    try:
        SampleRecord(
            "data/cat_001.jpg",
            "cat",
            123
        )
        print("测试失败：应该抛出异常")
    except TypeError as e:
        print("测试通过：", e)


if __name__ == "__main__":
    main()
