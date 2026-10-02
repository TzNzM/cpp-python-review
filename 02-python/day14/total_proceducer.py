from turtle import forward

import torch as th
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split, Subset
from ToyClassficationDataset import ToyClassificationDataset
from pathlib import Path

class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim,output_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim,hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim,output_dim)
        )

    def forward(self,x):
        return self.net(x)

def main():
    checkpoint_path = Path(__file__).with_name("best_model.pt")
    best_accuracy = -1.0
    th.manual_seed(42)

    num_per_class = 100

    # 类别 0：聚集在 (-1, -1) 附近
    x0 = th.randn(num_per_class, 2) * 0.2 + th.tensor([-1.0, -1.0])

    # 类别 1：聚集在 (1, 1) 附近
    x1 = th.randn(num_per_class, 2) * 0.2 + th.tensor([1.0, 1.0])

    X = th.cat([x0, x1], dim=0)

    Y = th.cat([
        th.zeros(num_per_class, dtype=th.long),
        th.ones(num_per_class, dtype=th.long),
    ], dim=0)

    # train_size = int(0.8 * len(X))
    # tcd_train = ToyClassificationDataset(X[:train_size],Y[:train_size])
    # tcd_test = ToyClassificationDataset(X[train_size:],Y[train_size:])

    full_dataset = ToyClassificationDataset(X, Y)

    train_size = int(0.8 * len(full_dataset))
    test_size = len(full_dataset) - train_size

    split_generator = th.Generator().manual_seed(42)
    tcd_train, tcd_test = random_split(
        full_dataset,
        [train_size, test_size],
        generator=split_generator,
    )

    train_loader = DataLoader(
        dataset=tcd_train,
        shuffle=True,
        batch_size=8,
        drop_last=False
    )

    test_loader = DataLoader(
        dataset=tcd_test,
        shuffle=False,
        batch_size=8,
        drop_last=False
    )
    num_epoch = 10
    input_dim, output_dim,hidden_dim = 2,8,2
    model = MLP(input_dim, output_dim,hidden_dim)
    critirion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(),lr=1e-3)

    # 新增：完整训练前，先用固定 8 个训练样本验证训练管线能否过拟合。
    small_dataset = Subset(tcd_train, range(8))
    small_loader = DataLoader(small_dataset, batch_size=8, shuffle=True)
    overfit_model = MLP(input_dim, output_dim, hidden_dim)
    overfit_optimizer = optim.Adam(overfit_model.parameters(), lr=1e-2)

    for _ in range(200):
        overfit_model.train()
        for batch_x, batch_y in small_loader:
            overfit_logits = overfit_model(batch_x)
            overfit_loss = critirion(overfit_logits, batch_y)
            overfit_optimizer.zero_grad()
            overfit_loss.backward()
            overfit_optimizer.step()

    overfit_model.eval()
    small_correct = 0
    small_total = 0
    with th.no_grad():
        for batch_x, batch_y in small_loader:
            small_predictions = th.argmax(overfit_model(batch_x), dim=1)
            small_correct += (small_predictions == batch_y).sum().item()
            small_total += batch_y.size(0)

    small_accuracy = small_correct / small_total
    print(f"8 样本过拟合 accuracy: {small_accuracy:.2%}")
    assert small_accuracy == 1.0, "8 样本未能过拟合，请先检查训练管线"

    for epoch in range(num_epoch):
        total_size = 0
        total_loss = 0.0
        model.train()
        for batch_x,batch_y in train_loader:
            outputs = model.forward(batch_x)
            loss = critirion(outputs,batch_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * batch_y.size(0)
            total_size += batch_y.size(0)
        avg_loss = total_loss / total_size
        model.eval()
        with th.no_grad():
            correct = 0
            total = 0
            for batch_x,batch_y in test_loader:
                target = model.forward(batch_x)
                outputs = th.argmax(target,dim=1)
                mask = outputs == batch_y
                correct += th.sum(mask).item()
                total += batch_y.size(0)
            val_accuracy = correct / total

            if val_accuracy > best_accuracy:
                best_accuracy = val_accuracy
                th.save(model.state_dict(), checkpoint_path)

            print(
                f"Epoch {epoch + 1}: "
                f"train_loss={avg_loss:.4f}, "
                f"val_accuracy={val_accuracy:.2%}"
            )

if __name__ == "__main__":
    main()
