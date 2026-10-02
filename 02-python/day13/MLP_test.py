import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(2,4),
    nn.ReLU(),
    nn.Linear(4,3)
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


logits = model.forward(x)

labels = torch.tensor(
    [0, 1, 2, 1],
    dtype=torch.long
)

criterion = nn.CrossEntropyLoss()
loss = criterion(logits,labels)
print("loss:", loss.item())