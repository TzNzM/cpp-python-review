# def build_sample_summary(samples:list):
#     paths = []
#     counts = {}
#     labels = set()

#     for sample in samples:
#         if sample.get("valid"):
#             if sample.get("path").strip().lower().endswith(".jpg"):
#                 if not (sample.get("label") is None):
#                     paths.append(sample.get("path"))
#                     labels.add(sample.get("label").strip())
#                     if counts.get(sample.get("label")):
#                         counts[sample.get("label")] += 1
#                     else:
#                         counts[sample.get("label")] = 1
#     return {
#         "paths":paths,
#         "counts":counts,
#         "labels":labels
#     }

def build_sample_summary(samples: list) -> dict:
    qualified_samples = [
        {
            "path": sample["path"].strip(),
            "label": sample["label"].strip(),
        }
        for sample in samples
        if sample.get("valid") is True
        and isinstance(sample.get("path"), str)
        and sample["path"].strip().lower().endswith(".jpg")
        and isinstance(sample.get("label"), str)
        and sample["label"].strip()
    ]

    paths = [sample["path"] for sample in qualified_samples]

    labels = {sample["label"] for sample in qualified_samples}

    counts = {
        label: sum(sample["label"] == label for sample in qualified_samples)
        for label in labels
    }

    return {
        "paths": paths,
        "counts": counts,
        "labels": labels,
    }

def main():
    samples = [
        {"path": " train/cat_001.jpg ", "label": "cat", "valid": True},
        {"path": "train/dog_001.jpg", "label": "dog", "valid": True},
        {"path": "val/cat_002.png", "label": "cat", "valid": True},
        {"path": "test/bird_001.jpg", "label": "bird", "valid": False},
        {"path": "train/dog_002.jpg", "label": "dog", "valid": True},
        {"path": "train/cat_bad.txt", "label": "cat", "valid": True},
    ]
    results = build_sample_summary(samples)
    print(results)

if __name__ == "__main__":
    main()