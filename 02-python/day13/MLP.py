import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(2, 4),
    nn.ReLU(),
    nn.Linear(4, 3)
)


# =========================
# 2. 输入
# =========================

x = torch.tensor([
    [1.0, 2.0],
    [2.0, 1.0],
    [3.0, 2.0],
    [1.0, 3.0],
])

print("\nx.shape:", x.shape)

# =========================
# 3. forward
# =========================

logits = model(x)

print("logits:")
print(logits)

print("logits.shape:", logits.shape)


# =========================
# 4. 标签
# =========================

labels = torch.tensor(
    [0, 1, 2, 1],
    dtype=torch.long
)

print("labels:", labels)
print("labels.shape:", labels.shape)
print("labels.dtype:", labels.dtype)

# =========================
# 5. CrossEntropyLoss
# =========================

criterion = nn.CrossEntropyLoss()

loss = criterion(logits, labels)

print("loss:", loss.item())


# =========================
# 6. 基本断言
# =========================

assert x.shape == (4, 2)
assert logits.shape == (4, 3)

assert labels.shape == (4,)
assert labels.dtype == torch.long

print("\n正确标签测试通过！")

# 新增：float 标签不符合 CrossEntropyLoss 对 class-index 标签必须为 torch.long 的要求。
float_labels = labels.to(dtype=torch.float32)
try:
    criterion(logits, float_labels)
except RuntimeError as error:
    print("float 标签测试通过：", error)
else:
    raise AssertionError("float 标签应触发 RuntimeError")

# 新增：shape 为 (N, 1) 的标签不符合 CrossEntropyLoss 需要 (N,) 标签的要求。
wrong_shape_labels = labels.unsqueeze(1)
try:
    criterion(logits, wrong_shape_labels)
except RuntimeError as error:
    print("错误 shape 标签测试通过：", error)
else:
    raise AssertionError("shape 为 (N, 1) 的标签应触发 RuntimeError")
