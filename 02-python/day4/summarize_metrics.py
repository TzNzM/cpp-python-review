def summarize_metrics(*values, **options):
    if len(values) == 0:
        raise ValueError("Value为空")
    precision = options.pop("precision", 4)
    name = options.pop("name", "metric")
    metadata = options
    count = len(values)
    Min = min(values)
    Max = max(values)
    sum = 0.0
    for value in values:
        # if min > value:
        #     min = value
        # if max < value:
        #     max = value
        sum += value    
    mean = sum / count
    sum = round(sum,precision)
    mean = round(mean,precision)

    results = {
        "name":name,
        "count":count,
        "sum":sum,
        "min":Min,
        "max":Max,
        "mean":mean,
        "metadata":metadata
    }
    return results

def main():
    resullts = summarize_metrics(
        0.75, 0.80, 0.90,
        name="accuracy",
        precision=3,
        epoch=2,
        split="validation",
    )
    print(resullts)
    resullts = summarize_metrics(
            0.75,
        )
    print(resullts)

if __name__ == "__main__":
    main()