from sample_record import SampleRecord

class Batch:
    def __init__(self,sampleRecord_list) -> None:
        self._sampleRecord_list = []
        for sampleRecord in sampleRecord_list:
            if isinstance(sampleRecord, SampleRecord):
                self._sampleRecord_list.append(sampleRecord)
            else:
                raise TypeError("不是SampleRecord类")

    def __len__(self):
        return len(self._sampleRecord_list)

    def __getitem__(self, key):
        return self._sampleRecord_list[key]

    def __iter__(self):
        # return iter(self._sampleRecord_list)
        for record in self._sampleRecord_list:
            yield record

    def __repr__(self) -> str:
        return "Batch(size=%d)" % len(self._sampleRecord_list)

    def __str__(self) -> str:
        return f"Batch: {len(self._sampleRecord_list)} records"

class BaseRecord:
    def __init__(self, path):
        self.path = path

class LabeledRecord(BaseRecord):
    def __init__(self, path, label):
        super().__init__(path)
        self.label = label


def main():
    records = [
        SampleRecord("data/cat_001.jpg", "cat", "cat"),
        SampleRecord("data/dog_001.jpg", "dog", "cat"),
        SampleRecord("data/bird_001.jpg", "bird"),
    ]
    batch = Batch(records)
    print(len(batch))
    print(batch[0])
    print(list(batch))
    print(batch)
    print(repr(batch))
    try:
        Batch([
            SampleRecord("data/cat_001.jpg", "cat"),
            "not a sample record",
        ])
    except TypeError as error:
        print("测试通过：", error)

    try:
        print(batch[10])
    except IndexError as error:
        print("测试通过：", error)

    # super() 用于沿继承链查找并调用父类的方法；
    # 这里要调用的是父类的 __init__，即 super().__init__(path)。
    # 子类重写了 __init__ 后，如果不主动调用它，父类初始化逻辑不会自动执行，所以 path 根本没有创建。
    print(LabeledRecord("a.jpg", "cat").path)

if __name__ == "__main__":
    main()