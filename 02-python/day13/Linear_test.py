import torch

# =========================
# 1. 数据
# =========================

x = torch.tensor(
    [1.0, 2.0, 3.0, 4.0],
    dtype=torch.float32
)

y = torch.tensor(
    [3.0, 5.0, 7.0, 9.0],
    dtype=torch.float32
)

w = torch.tensor(
    0.0,
    dtype=torch.float32,
    requires_grad=True
)

b = torch.tensor(
    0.0,
    dtype=torch.float32,
    requires_grad=True
)

learning_rate = 0.01
prediction = x * w + b
loss_before = torch.mean((y - prediction)**2)

if w.grad is not None:
    w.grad.zero_()
if b.grad is not None:
    b.grad.zero_()

loss_before.backward()

with torch.no_grad():
    w = w - w.grad * learning_rate
    b = b - b.grad * learning_rate

prediction_after = x * w + b
loss_after = torch.mean((y - prediction_after)**2)
if loss_after < loss_before:
    print("success")
else:
    print("failed")