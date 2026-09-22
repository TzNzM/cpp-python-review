
class MetricTracker:
    def __init__(self, name="metric"):
        self._name = name
        self._accculative_sum = 0
        self._n_sample = 0
        self._b_update = False

    def update(self, value, n=1):
        if n <= 0:
            raise ValueError("n不能小于等于0")
        self._accculative_sum += n * value
        self._n_sample += n
        self._b_update = True

    def average(self):
        if not self._b_update:
            return None
        else:
            return self._accculative_sum / self._n_sample

    def reset(self):
        self._accculative_sum = 0
        self._n_sample = 0
        self._b_update = False


class Experiment:
    tag = "baseline"

    def __init__(self, name):
        self.name = name

def main():
    tracker = MetricTracker("accuracy")
    tracker.update(0.8,2)
    tracker.update(1,1)
    print(tracker.average())

    a = Experiment("a")
    b = Experiment("b")
    a.tag = "trial-a" # 因为 a.tag = "trial-a" 在 a 上创建了实例属性，遮蔽类属性；b 没有同名实例属性，因此读取更新后的 Experiment.tag。
    Experiment.tag = "v2"
    print(a.tag)
    print(b.tag)
    print(Experiment.tag)


if __name__ == "__main__":
    main()
