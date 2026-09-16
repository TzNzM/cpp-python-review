
def compare_splits(train_paths, val_paths):
    train = set()
    val = set()
    train_duplicates = set()
    val_duplicates = set()

    for train_path in train_paths:
        if train_path in train:
            train_duplicates.add(train_path)
        else:
            train.add(train_path)
    for val_path in val_paths:
        if val_path in val:
            val_duplicates.add(val_path)
        else:
            val.add(val_path)
    shared = val & train
    train_only = train - shared
    val_only = val - shared

    results = {
        "shared":shared,
        "train_only":train_only,
        "val_only":val_only,
        "train_duplicates":train_duplicates,
        "val_duplicates":val_duplicates
    }
    return results


def main():
    train_paths = [
        "cat_001.jpg",
        "dog_002.jpg",
        "bird_003.jpg",
        "dog_002.jpg",
    ]

    val_paths = [
        "dog_002.jpg",
        "fish_004.png",
        "dog_002.jpg",
    ]

    results = compare_splits(train_paths, val_paths)
    for key,value in results.items():
        print(key,value)


if __name__ == "__main__":
    main()