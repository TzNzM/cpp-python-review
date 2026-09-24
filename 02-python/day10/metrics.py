from collections import Counter
def count_labels(items : list[tuple[str,str]]) -> dict[str,int]:
    counter = Counter(label for _,label in items)
    return counter