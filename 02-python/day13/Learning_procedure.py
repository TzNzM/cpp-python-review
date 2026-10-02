from turtle import forward

import torch as th
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader,TensorDataset


class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(MLP,self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim,hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim,hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim,output_dim)
        )

    def forward(self, x):
        return self.net(x)

x = th.randn(1000,20) # 1000个样本，20个特征
# y = th.randint(0,4,(1000,)) # 原代码：只生成 0 到 3，和 5 类输出不一致。
# 修改：5 类任务的合法标签范围应为 0 到 4。
y = th.randint(0,5,(1000,))

train_size = int(0.8 * len(x))
train_dataset = TensorDataset(x[0:train_size],y[0:train_size])
# test_dataset = TensorDataset(x[train_size:-1],y[train_size:-1]) # 原代码：切片 -1 会遗漏最后一个样本。这里主要是开闭区间的问题
# 修改：测试集应从 train_size 一直包含到结尾。
test_dataset = TensorDataset(x[train_size:],y[train_size:])

train_loader = DataLoader(dataset=train_dataset,batch_size=32,shuffle=True)
test_loader = DataLoader(dataset=test_dataset,batch_size=32,shuffle=False)

# 开始初始化模型
input_dim, hidden_dim, output_dim = 20,64,5
model = MLP(input_dim, hidden_dim, output_dim)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(),lr=1e-3)
epoch_num = 10
# 训练阶段
for epoch in range(epoch_num):
    model.train()
    running_loss = 0.0
    for batch_x,batch_y in train_loader:
        outputs = model.forward(batch_x)
        loss = criterion(outputs,batch_y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # running_loss += loss # 原代码：累计带计算图的 Tensor，可能保留不必要的计算图。
        # 修改：只累计用于日志的 Python 标量，不保留计算图。
        running_loss += loss.item()
    avg_loss = running_loss / len(train_loader)
    print(f"running epoch:{epoch + 1}/{epoch_num},avg_loss:{avg_loss}")
# 测试阶段
model.eval()
correct = 0
total = 0
with th.no_grad():
    for batch_x,batch_y in test_loader:
        outputs = model.forward(batch_x) # [B,5]
        # _,predicted = th.max(outputs.data,1)
        predicted = th.argmax(outputs.data,1)
        total += batch_x.size(0)
        # print((predicted == batch_y).sum())
        correct += (predicted == batch_y).sum().item()
print(f"Test Accuracy:{(100*(correct / total)):.2f}%")


