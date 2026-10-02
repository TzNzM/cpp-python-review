import numpy as np
import torch
import torch.nn.functional as F

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
    # =========================
    # 1. 准备数据
    # =========================

    logits_np = np.array([
        [2.0, 1.0, 0.1],
        [0.2, 3.0, 1.0],
        [1.0, 0.5, 2.5],
        [3.0, 0.2, 1.0],
        [0.1, 0.5, 2.0],
        [1.5, 2.0, 0.3],
    ], dtype=np.float32)

    labels_np = np.array([0, 1, 2, 0, 2, 1], dtype=np.int64)

    # Numpy 版本
    probs_np = softmax(logits_np)

    print("softmax:")
    print(probs_np)

    prediction_np = probs_np.argmax(axis=1)
    mask_np = (prediction_np == labels_np)
    accuracy_np = mask_np.sum() / len(mask_np)

    print(f"accuracy:{accuracy_np}")

    print("每行概率和:")
    print(probs_np.sum(axis=1))

    print("cross entropy:")
    print(cross_entropy(logits_np, labels_np))

    # Tensor 版本
    # =========================
    # 3. Tensor + device
    # =========================

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    logits = torch.tensor(logits_np, dtype=torch.float32, device=device)
    labels = torch.tensor(labels_np, dtype=torch.long, device=device)

    probs = F.softmax(logits,dim=-1)
    print(f"torch probobility:{probs}")
    print("每行概率和:")
    print(probs.sum(axis=1))

    predictions = torch.argmax(probs, dim=1)

    accuracy = (predictions == labels).float().mean()


    # =========================
    # 4. 打印信息
    # =========================

    print("\nTensor:")
    print("logits:", logits)
    print("logits.shape:", logits.shape)
    print("logits.dtype:", logits.dtype)
    print("logits.device:", logits.device)

    print("labels:", labels)
    print("labels.shape:", labels.shape)
    print("labels.dtype:", labels.dtype)
    print("labels.device:", labels.device)

    print("predictions:", predictions)
    print("predictions.shape:", predictions.shape)
    print("predictions.dtype:", predictions.dtype)
    print("predictions.device:", predictions.device)

    print("Tensor accuracy:", accuracy.item())


    # =========================
    # 5. 断言
    # =========================

    assert logits.shape == (6, 3)
    assert labels.shape == (6,)
    assert predictions.shape == (6,)

    assert logits.dtype == torch.float32
    assert labels.dtype == torch.long
    assert predictions.dtype == torch.long

    assert logits.device == device
    assert labels.device == device
    assert predictions.device == device

    assert np.isclose(accuracy.item(), accuracy_np)

    print("\n练习 1 第一部分通过！")


if __name__ == "__main__":
    main()
