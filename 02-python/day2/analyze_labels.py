def analyze_labels(labels): 
    counts = {}
    first_indices = {}
    for i in range(len(labels)):
        if counts.get(labels[i]) is None:#第一次出现
            first_indices[labels[i]] = i
            counts[labels[i]] = 1
        else:
            counts[labels[i]] += 1
    d = {"counts":counts,"first_indices":first_indices}
    return d


def main():
    labels = ["cat", "dog", "cat", "bird", "dog", "cat"]
    # labels = ["cat","cat","cat"]
    results = analyze_labels(labels)
    for key,value in results.items():
        print(key,value)

if __name__ == "__main__":
    main()