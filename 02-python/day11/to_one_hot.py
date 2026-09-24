import numpy as np

def to_one_hot(labels: np.ndarray, num_classes: int) -> np.ndarray:
    if labels.ndim != 1:
        raise ValueError("labels 维度不正确")
    if not np.issubdtype(labels.dtype, np.integer):
        raise TypeError(
            f"labels 必须是整数 dtype，当前为 {labels.dtype}"
        )
    masks_1 = labels >= 0
    masks_2 = labels < num_classes
    masks = masks_1 & masks_2 
    if masks.all() == True:
        one_hot = np.zeros((len(labels),num_classes),dtype=np.float32)
        one_hot[np.arange(len(labels)),labels] = 1
        return one_hot
    else:
        raise ValueError("labels 数值不正确")


def main():
    # =========================
    # 1. 正常输入
    # =========================

    labels = np.array([0, 2, 1, 2])

    result = to_one_hot(labels, num_classes=3)

    print("正常输入：")
    print(result)

    assert result.shape == (4, 3)
    assert result.dtype == np.float32
    assert np.array_equal(
        result,
        np.array([
            [1, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 0, 1]
        ], dtype=np.float32)
    )

    # =========================
    # 2. 空标签
    # =========================

    empty_labels = np.array([], dtype=np.int64)

    result = to_one_hot(empty_labels, num_classes=3)

    assert result.shape == (0, 3)
    assert result.ndim == 2
    assert result.dtype == np.float32

    print("空标签：测试通过")


    # =========================
    # 3. 浮点标签
    # =========================

    try:
        to_one_hot(
            np.array([0.0, 1.0, 2.0]),
            num_classes=3
        )
    except (ValueError, IndexError, TypeError) as e:
        print("浮点标签：正确捕获异常 ->", e)


    # =========================
    # 4. 二维标签
    # =========================

    try:
        to_one_hot(
            np.array([[0, 1], [2, 0]]),
            num_classes=3
        )
    except ValueError as e:
        print("二维标签：正确捕获异常 ->", e)


    # =========================
    # 5. 包含 -1
    # =========================

    try:
        to_one_hot(
            np.array([0, -1, 2]),
            num_classes=3
        )
    except ValueError as e:
        print("包含 -1：正确捕获异常 ->", e)


    # =========================
    # 6. 包含 num_classes
    # =========================

    try:
        to_one_hot(
            np.array([0, 1, 3]),
            num_classes=3
        )
    except ValueError as e:
        print("包含 num_classes：正确捕获异常 ->", e)


if __name__ == "__main__":
    main()