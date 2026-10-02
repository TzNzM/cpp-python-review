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

# =========================
# 2. 初始化参数
# =========================

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

# =========================
# 3. 更新前 forward
# =========================
learning_rate = 0.01

prediction = w * x + b

loss_before = torch.mean(
    (prediction - y) ** 2
)

print("更新前 loss:", loss_before.item())
print("更新前 w:", w.item())
print("更新前 b:", b.item())


# =========================
# 4. 清除梯度
# =========================

if w.grad is not None:
    w.grad.zero_()

if b.grad is not None:
    b.grad.zero_()

# =========================
# 5. 反向传播
# =========================

loss_before.backward()

print("\nw.grad:", w.grad)
print("b.grad:", b.grad)


# =========================
# 6. 保存更新前参数
# =========================

w_before = w.detach().clone()
b_before = b.detach().clone()

# =========================
# 7. 参数更新
# =========================

with torch.no_grad():
    w -= learning_rate * w.grad
    b -= learning_rate * b.grad

# =========================
# 8. 更新后重新计算 loss
# =========================

prediction_after = w * x + b

loss_after = torch.mean(
    (prediction_after - y) ** 2
)

print("\n更新后:")
print("w:", w.item())
print("b:", b.item())
print("loss:", loss_after.item())


# =========================
# 9. 断言
# =========================

assert not torch.equal(w, w_before)
assert not torch.equal(b, b_before)

assert loss_after.item() < loss_before.item()

print("\n练习 2A 通过！")