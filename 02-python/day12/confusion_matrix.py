import numpy as np

def normalize_nchw(images: np.ndarray) -> np.ndarray:
    mean = images.mean(axis=(0,2,3),keepdims=True)
    std = images.std(axis=(0,2,3),keepdims=True)
    if np.any(std == 0):
        raise ValueError("有通道的std为0")
    normalized = (images - mean) / std
    return normalized
def accuracy(predictions: np.ndarray, targets: np.ndarray) -> float:
    mask = predictions == targets
    correct = np.sum(mask)
    accuracy = correct / len(mask)
    return accuracy

def confusion_matrix(
    predictions: np.ndarray,
    targets: np.ndarray,
    num_classes: int,
) -> np.ndarray:
    matrix = np.zeros((num_classes,num_classes),dtype=int)
    # 按照 targets 指定行、predictions 指定列，把对应位置各加 1。
    np.add.at(matrix, (targets, predictions), 1)
    return matrix



def main():
    predictions = np.array([0, 2, 1, 2, 0, 1])
    targets = np.array([0, 1, 1, 2, 0, 2])
    print(f"accuracy:{accuracy(predictions=predictions,targets=targets)}")
    images = np.arange(4 * 3 * 2 * 2, dtype=np.float32).reshape(4, 3, 2, 2)
    normalized = normalize_nchw(images)
    assert np.allclose(normalized.mean(axis=(0, 2, 3)), 0.0, atol=1e-6)
    assert np.allclose(normalized.std(axis=(0, 2, 3)), 1.0, atol=1e-6)
    print(normalized)
    print(confusion_matrix(predictions,targets,num_classes=3))

if __name__ == "__main__":
    main()
