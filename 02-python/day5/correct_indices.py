def find_correct_indices(predictions, labels):
    if len(predictions) != len(labels):
        raise ValueError("长度不一致")
    pairs = zip(predictions,labels)
    return [indice for indice,x in enumerate(pairs) if x[0] == x[1]]

def main():
    predictions = [2, 0, 1, 1, 3]
    labels = [2, 1, 1, 0, 3]
    results = find_correct_indices(predictions,labels)
    print(results)

    matrix = [[3, -1, 2], [], [0, 5]]
    flat_positive = [value for row in matrix for value in row if value > 0]
    print(flat_positive)

    new_flat_positive = []
    for row in matrix:
        for value in row:
            if value > 0:
                new_flat_positive.append(value)
    print(new_flat_positive)

if __name__ == "__main__":
    main()