import numpy as np

def _validate_logits(logits: np.ndarray) -> None:
    if logits.ndim != 2:
        raise ValueError("logits 必须是 shape 为 (N, C) 的二维数组")
    if logits.shape[0] == 0:
        raise ValueError("logits 不能为空")
    if logits.shape[1] == 0:
        raise ValueError("logits 至少需要一个类别")


def _validate_targets(targets: np.ndarray, batch_size: int, num_classes: int) -> None:
    if targets.ndim != 1:
        raise ValueError("targets 必须是一维数组")
    if targets.shape[0] != batch_size:
        raise ValueError("targets 长度必须等于 batch size")
    if not np.issubdtype(targets.dtype, np.integer):
        raise TypeError("targets 必须是整数 dtype")
    if np.any(targets < 0) or np.any(targets >= num_classes):
        raise ValueError("targets 存在越界类别索引")


def softmax(logits: np.ndarray) -> np.ndarray:
    _validate_logits(logits)
    logits_max = logits.max(axis=1, keepdims=True)

    shifted = logits - logits_max

    exp_values = np.exp(shifted)

    return exp_values / exp_values.sum(axis=1, keepdims=True)

def cross_entropy(logits: np.ndarray, targets: np.ndarray) -> float:
    _validate_logits(logits)
    _validate_targets(targets, logits.shape[0], logits.shape[1])

    shifted = logits - logits.max(axis=1, keepdims=True)
    log_probs = shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))
    return float(-np.mean(log_probs[np.arange(targets.shape[0]), targets]))

def main():
    logits = np.array([
        [1000.0, 1001.0, 999.0],
        [-1000.0, -999.0, -1001.0],
        [0.0, 0.0, 0.0],
    ])

    targets = np.array([1, 0, 2])

    probs = softmax(logits)

    print("softmax:")
    print(probs)

    print("每行概率和:")
    print(probs.sum(axis=1))

    print("cross entropy:")
    print(cross_entropy(logits, targets))

    extreme_logits = np.array([[10000.0, -10000.0]])
    extreme_loss = cross_entropy(extreme_logits, np.array([1]))
    assert np.isfinite(extreme_loss)
    assert np.isclose(extreme_loss, 20000.0)
    print("极端 logits loss:", extreme_loss)

if __name__ == "__main__":
    main()
