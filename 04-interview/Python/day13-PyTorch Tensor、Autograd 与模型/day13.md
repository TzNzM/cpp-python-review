面试题：
1. torch.tensor()、torch.from_numpy() 和 Tensor.numpy() 分别如何处理内存？哪些情况会共享内存？
torch.tensor(data) 默认会复制数据，创建独立 Tensor；修改原数据通常不会影响它。
torch.from_numpy(array) 与 CPU 上的 NumPy 数组共享底层内存。修改 NumPy 数组会影响 Tensor，修改 Tensor 也会影响 NumPy 数组。
tensor.numpy() 在 Tensor 位于 CPU、无需梯度且满足转换条件时，返回与 Tensor 共享内存的 NumPy 数组。若 Tensor 正在跟踪梯度，通常先写：
tensor.detach().cpu().numpy()
2. requires_grad=True、计算图与 backward() 分别是什么关系？为什么通常只需要对可训练参数开启梯度？
对 Tensor 设置 requires_grad=True 后，PyTorch 会记录其参与的可微分运算，形成计算图。
loss.backward() 会从 loss 沿计算图反向传播，按链式法则计算梯度；叶子参数的梯度累积在 .grad 中。
通常只为可训练参数开启梯度，因为输入数据、标签等不需要被优化。无关 Tensor 追踪梯度会增加计算量和显存占用。例外是对输入求梯度的场景，如对抗样本或可解释性分析。
3. PyTorch 为什么默认累加梯度？训练循环中为什么要调用 zero_grad()？
PyTorch 默认将新梯度累加到已有 .grad，这支持多个 loss 共同反传、梯度累积模拟大 batch 等场景。
因此普通训练循环中，每一轮反向传播前都要清梯度：
optimizer.zero_grad()
loss.backward()
optimizer.step()
否则本轮梯度会叠加上一轮梯度，参数更新不再只由当前 batch 的 loss 决定。optimizer.step() 不会自动清零梯度。
4. detach()、torch.no_grad() 与 model.eval() 分别解决什么问题？它们能互相替代吗？
detach() 返回一个与原 Tensor 脱离计算图的 Tensor；它通常仍共享数据，但后续操作不再向原计算图传梯度。
torch.no_grad() 是上下文管理器，在其代码块内停止记录计算图，常用于验证和推理，能减少显存与计算开销。它不永久修改参数的 requires_grad。
model.eval() 将模型切换到评估行为，主要影响 Dropout 和 BatchNorm；它不会关闭梯度，也不会阻止 optimizer.step() 更新参数。
不能互相替代
5. CrossEntropyLoss 对 logits 和标签的 shape、dtype 有什么要求？为什么分类模型输出后通常不能先做 softmax？
最常见的单标签多分类场景：
- logits：shape 为 (N, C)，dtype 通常为 torch.float32；是未经 softmax 的原始分数。
- targets：shape 为 (N,)，dtype 必须为 torch.long；每个值是 [0, C) 内的类别索引。
因此标签不应和 logits 保持相同 shape 或 dtype。比如 3 类、4 个样本：
logits.shape   # (4, 3)
targets.shape  # (4,)
targets.dtype  # torch.int64 / torch.long
模型输出 logits 不是“已经选择好的类别”，而是每个类别的原始评分。CrossEntropyLoss 内部已经完成数值稳定的 log_softmax + NLLLoss。如果先手动做 softmax，会改变它预期的输入形式，并可能降低数值稳定性。