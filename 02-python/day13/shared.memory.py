import numpy as np
import torch


# =========================
# 1. NumPy → Tensor
# =========================

array = np.array([1.0, 2.0, 3.0], dtype=np.float32)

tensor = torch.from_numpy(array)

print("原始 array:", array)
print("原始 tensor:", tensor)


# =========================
# 2. 修改 NumPy
# =========================

array[0] = 100.0

print("\n修改 NumPy 后:")
print("array:", array)
print("tensor:", tensor)

assert tensor[0].item() == 100.0


# =========================
# 3. clone
# =========================

tensor_clone = tensor.clone()

print("\nclone:")
print("tensor:", tensor)
print("tensor_clone:", tensor_clone)


# =========================
# 4. 再修改原 NumPy
# =========================

array[1] = 200.0

print("\n再次修改 NumPy 后:")
print("array:", array)
print("tensor:", tensor)
print("tensor_clone:", tensor_clone)

assert tensor[1].item() == 200.0
assert tensor_clone[1].item() != 200.0

print("\n共享内存实验通过！")