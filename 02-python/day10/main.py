from data_utils import read_labels,write_label_summary
from pathlib import Path

def main():
    base_dir = Path(__file__).parent
    items = read_labels(base_dir / "labels_valid.txt")
    print(items)
    write_label_summary(items,base_dir / "existing_summary.txt")

if __name__ == "__main__":
    main()