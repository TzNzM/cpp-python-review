class SampleRecord:
    def __init__(self, path, label, prediction=None):
        path = path.strip()
        if isinstance(path,str) and path is not None and path != "":
            self._path = path
        else:
            raise TypeError("类型不正确或为空")
        label = label.strip()
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

    # __getattr__：只有正常找不到属性时才触发。
    # __setattr__：所有属性赋值都会经过它，影响范围很大。
    # @property：只精确控制 label 这一个属性，更符合“受控标签 property”的任务目标。
    # def __getattr__(self, name):
    #     if name == "label":
    #         return self._label
    #     else:
    #         object.__getattribute__(self,name)

    # def __setattr__(self, name: str, value: str) -> None:
    #     if name == "label":
    #         value = value.strip()
    #         if value == "dog" or value == "cat" or value == "bird":
    #             self._label = value
    #         else:
    #             raise ValueError("不合法输入")
    #     else:
    #         object.__setattr__(self,name,value)

    @property
    def label(self):
        return self._label
    # 这里 label 是对外暴露的属性名，_label 是实际存储值的内部属性名。
    @label.setter
    def label(self,value):
        if not isinstance(value, str):
            raise TypeError("label 必须是字符串")

        value = value.strip()
        if value not in {"cat", "dog", "bird"}:
            raise ValueError("不合法标签")

        self._label = value


    def __repr__(self) -> str:
        return "path:" + str(self._path) + ",label:" + str(self._label) + ",prediction:" + str(self._prediction)
        
def main():
    # # 1. 合法样本
    # print("测试1：合法样本")
    # sample = SampleRecord(
    #     " data/cat_001.jpg ",
    #     "cat"
    # )

    # print(sample._path)
    # print(sample._label)
    # print(sample._prediction)
    # print()


    # # 2. 预测正确
    # print("测试2：预测正确")
    # sample = SampleRecord(
    #     "data/cat_001.jpg",
    #     "cat",
    #     "cat"
    # )

    # print(sample.is_correct())
    # assert sample.is_correct() is True
    # print("测试通过")
    # print()


    # # 3. 预测错误
    # print("测试3：预测错误")
    # sample = SampleRecord(
    #     "data/cat_001.jpg",
    #     "cat",
    #     "dog"
    # )

    # print(sample.is_correct())
    # assert sample.is_correct() is False
    # print("测试通过")
    # print()


    # # 4. 空路径
    # print("测试4：空路径")
    # try:
    #     SampleRecord(
    #         "",
    #         "cat"
    #     )
    #     print("测试失败：应该抛出异常")
    # except TypeError as e:
    #     print("测试通过：", e)
    # print()


    # # 5. 空标签
    # print("测试5：空标签")
    # try:
    #     SampleRecord(
    #         "data/cat_001.jpg",
    #         ""
    #     )
    #     print("测试失败：应该抛出异常")
    # except TypeError as e:
    #     print("测试通过：", e)
    # print()


    # # 6. 非法预测
    # print("测试6：非法预测")
    # try:
    #     SampleRecord(
    #         "data/cat_001.jpg",
    #         "cat",
    #         123
    #     )
    #     print("测试失败：应该抛出异常")
    # except TypeError as e:
    #     print("测试通过：", e)

    record = SampleRecord(" data/cat_001.jpg ", "cat")
    print(record)
    record.label = "dog"
    assert record.label == "dog"

    try:
        record.label = "lion"
        
        # 写入 "lion" 与 "   " 时都应报错；
        # 报错后 record.label 仍为 "dog"
    except ValueError as e:
        print("测试通过：", e)
        print(record.label)
    assert record.label == "dog"
    try:
        record.label = "     "
        # 写入 "lion" 与 "   " 时都应报错；
        # 报错后 record.label 仍为 "dog"
    except ValueError as e:
        print("测试通过：", e)
        print(record.label)
    assert record.label == "dog"


if __name__ == "__main__":
    main()
