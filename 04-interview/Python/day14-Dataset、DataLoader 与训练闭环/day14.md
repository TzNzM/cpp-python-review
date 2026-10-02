面试题：
1. Dataset.__len__ 与 Dataset.__getitem__ 各自负责什么？为什么 __getitem__ 通常只返回一个样本？
Dataset.__len__返回当前datatset的数据大小。__getitem__负责返回当前的样本。
为什么 __getitem__ 通常只返回一个样本？因为这个通常只是为了能够通过索引去提取某一个具体的样本数据
Dataset.__getitem__(index) 根据索引返回一条样本，通常是 (feature, label)
2. DataLoader 的 shuffle、drop_last 分别解决什么问题？验证集是否应 shuffle=True？
shuffle会在每个 epoch 开始时随机打乱样本顺序，避免模型长期按固定顺序看到数据，通常训练集应开启。
drop_last=True 会丢弃最后一个不足 batch_size 的 batch；False 则保留它。训练中若依赖固定 batch size，例如某些 BatchNorm 或多卡场景，可能选择丢弃；验证时通常保留全部样本。
验证集通常不需要 shuffle=True，因为不更新参数，样本顺序不应影响最终平均 loss 和 accuracy。
3. model.train()、model.eval()、torch.no_grad() 分别影响什么？为什么验证时通常同时使用后两者？
model.train()使得模型在训练状态，主要影响 Dropout 和 BatchNorm：Dropout 会随机失活，BatchNorm 会更新运行统计量。
model.eval()使得模型在测试状态，Dropout 停止随机失活，BatchNorm 使用已保存的运行统计量。
torch.no_grad()在代码块中关闭计算图记录和梯度计算，减少显存及计算开销。它不等于“不更新参数”；真正更新参数的是 optimizer.step()。
验证时常同时使用：
model.eval()
with torch.no_grad():
    ...
前者保证模型层行为正确，后者避免无意义的梯度计算。
4. 为什么平均 loss 不能简单把每个 batch 的 loss 相加后除以 batch 数？最后一个 batch 较小时应如何正确计算？
大多数 loss 默认返回当前 batch 的平均 loss。若直接把每个 batch loss 相加后除以 batch 数，会让小 batch 和大 batch 权重相同。
最后一个 batch 往往更小，因此应按样本数加权：
total_loss += batch_loss * 当前 batch 样本数
average_loss = total_loss / 总样本数
这样每条样本对最终平均 loss 的贡献相同。
5. 为什么保存 state_dict 而不是整个模型对象？“小样本过拟合到 100%”为什么是训练管线的重要自检？
state_dict 保存模型参数和缓冲区组成的字典，例如权重、bias、BatchNorm 的统计量。保存它比保存整个模型对象更稳健：加载时只需先创建同样结构的模型，再加载参数。
保存完整模型对象通常依赖 Python pickle 和原始类的导入路径；项目重构、类改名或环境变化后，加载可能失败。对不可信文件，pickle 也有安全风险。
小样本过拟合到 100% 是训练管线自检：一个足够简单的小数据集理论上应能被模型记住。若做不到，常见问题包括标签错位、shape/dtype/device 错误、loss 用错、未调用 backward() 或 optimizer.step()、模型处于错误状态等。


Dropout 的作用是训练时随机把一部分神经元输出置为 0，防止模型过度依赖某些特征、降低过拟合风险。例如：
原输出： [2.0, 1.0, 3.0, 4.0]
训练模式： [2.0, 0.0, 3.0, 0.0]  # 每次随机结果可能不同
评估模式： [2.0, 1.0, 3.0, 4.0]  # 不再随机丢弃
所以模型在 train() 下，同一输入多次前向计算，Dropout 输出可能不同；在 eval() 下，输出应稳定。
BatchNorm 会对某层的特征做标准化。训练模式下，它使用“当前 batch”的均值和方差，同时更新一份长期保存的运行均值、运行方差；评估模式下，不再依赖当前验证 batch，而是使用训练阶段积累的运行统计量。
原因是验证 batch 可能很小，甚至最后一个 batch 只有 1 条样本。若仍使用当前 batch 的统计量，预测结果会随 batch 组成变化，不稳定。
典型流程是：
# 训练
model.train()
loss.backward()
optimizer.step()

# 验证 / 推理
model.eval()
with torch.no_grad():
    logits = model(inputs)
其中 train() / eval() 控制 Dropout、BatchNorm 的行为；no_grad() 控制是否构建计算图；optimizer.step() 才真正更新参数。