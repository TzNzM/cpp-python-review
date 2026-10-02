import torch as th
from torch.utils.data import DataLoader,Dataset

class ToyClassificationDataset(Dataset):
    def __init__(self,input_feature,label) -> None:
        self._input_feature = input_feature
        self._label = label

    def __len__(self):
        return len(self._input_feature)

    def __getitem__(self, index):
        return self._input_feature[index],self._label[index]


def main():
    th.manual_seed(42)

    num_per_class = 10

    # 类别 0：聚集在 (-1, -1) 附近
    x0 = th.randn(num_per_class, 2) * 0.2 + th.tensor([-1.0, -1.0])

    # 类别 1：聚集在 (1, 1) 附近
    x1 = th.randn(num_per_class, 2) * 0.2 + th.tensor([1.0, 1.0])

    X = th.cat([x0, x1], dim=0)

    Y = th.cat([
        th.zeros(num_per_class, dtype=th.long),
        th.ones(num_per_class, dtype=th.long),
    ], dim=0)

    N = len(X)


    tcd = ToyClassificationDataset(X,Y)
    print(len(tcd))
    print(tcd[1])

    dataloader = DataLoader(
        dataset=tcd,
        shuffle=True,
        batch_size=8,
        drop_last=False
    )
    total_without_drop = 0
    for batch_idx, (batch_x, batch_y) in enumerate(dataloader):
        total_without_drop += batch_y.size(0)
        print(f"\nBatch {batch_idx}")

        print("features shape:", batch_x.shape)
        print("labels shape:", batch_y.shape)

        print("features dtype:", batch_x.dtype)
        print("labels dtype:", batch_y.dtype)

        print("features device:", batch_x.device)
        print("labels device:", batch_y.device)

        print("label min:", batch_y.min().item())
        print("label max:", batch_y.max().item())

    droploader = DataLoader(
        dataset=tcd,
        shuffle=True,
        batch_size=8,
        drop_last=True
    )
    total_with_drop = 0
    for batch_idx, (batch_x, batch_y) in enumerate(droploader):
        total_with_drop += batch_y.size(0)
        print(f"\nBatch {batch_idx}")

        print("features shape:", batch_x.shape)
        print("labels shape:", batch_y.shape)

        print("features dtype:", batch_x.dtype)
        print("labels dtype:", batch_y.dtype)

        print("features device:", batch_x.device)
        print("labels device:", batch_y.device)

        print("label min:", batch_y.min().item())
        print("label max:", batch_y.max().item())

    print("total_with_drop:",total_with_drop)
    print("total_without_drop:",total_without_drop)

if __name__ == "__main__":
    main()