面试题：
1. shape、ndim、size、dtype 分别描述什么？为什么训练代码中应优先打印它们？
shape 就是数组的形状，每一维有多少数据
ndim 就是一共有多少维
size 是元素总数，是 shape 各维度的乘积；
dtype 每个元素的数据类型，例如 float32、int64。
优先打印他们能够更好的了解所要处理数据的维度这些问题
2. reshape 与 transpose 分别改变什么？它们是否一定复制数据？
reshape改变数组的形状，例如 (2, 3) 改为 (3, 2)；元素总数必须不变，它通常可返回 view，但原数组内存不连续时也可能复制数据。reshape 更适合元素总数不变、但确实要按连续顺序重新组织的情况，例如把 (N, C, H, W) 展平为 (N, C * H * W)。
transpose 交换或重排轴，例如图像从 NCHW 的 (N, C, H, W) 改为 NHWC 的 (N, H, W, C)。它通常返回 view，但结果经常变成非连续数组。
因此两者都不保证“绝不复制”。
3. 基本切片、布尔索引和整数数组索引，哪些通常返回 view，哪些通常返回 copy？
基本切片通常返回 view，例如：
part = array[1:4, :]
布尔索引和整数数组索引属于高级索引，通常返回 copy，例如：
array[array > 0]
array[[0, 2, 5]]
修改 view 往往会影响原数组；修改 copy 不会。最稳妥的独立副本写法是 .copy()。
4. squeeze 与 expand_dims 的用途是什么？为什么随意 squeeze() 可能意外删除 batch 维？
squeeze 删除长度为 1 的维度。例如 (1, 3, 224, 224) 经 squeeze() 可能变成 (3, 224, 224)。
expand_dims 在指定位置插入长度为 1 的维度。例如 (3, 224, 224) 在第 0 维扩展后变为 (1, 3, 224, 224)。
随意使用 squeeze() 的风险是：当 batch size 恰好为 1 时，会意外删掉 batch 维，导致模型期望四维输入却拿到三维输入。更安全的做法是指定轴，如 squeeze(axis=1)。
5. one-hot 标签的 shape 和 dtype 通常是什么？标签索引越界或 dtype 错误为什么会导致训练流程失败？
one-hot 通常形状为 (N, C)：N 是样本数，C 是类别数；常用 dtype 为 float32。
标签索引越界，例如类别数为 3 却出现标签 3，会访问不存在的类别列，通常直接报索引错误。标签 dtype 错误，例如浮点标签用于数组索引，会报索引类型错误或造成框架的 loss 输入类型错误。

补充：PyTorch 的 CrossEntropyLoss 通常接收 shape 为 (N,)、dtype 为 torch.long 的类别索引标签，而不是 one-hot；不能把 one-hot 当作所有分类损失函数的通用输入。