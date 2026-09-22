from pathlib import Path


def read_labels(path: Path) -> list[tuple[str, str]]:
    results = []
    with open(path,"r",encoding = "utf-8") as file:
        for line_number,line in enumerate(file,start=1):
            line = line.strip()
            if line == "":
                continue
            parts = line.split("\t")

            if len(parts) != 2:
                raise ValueError(
                    f"第{line_number}行：格式错误，应为 <路径>\\t<标签>"
                )

            data_path, label = parts
            data_path = data_path.strip()
            label = label.strip()
            if label == "" or data_path == "":
                raise ValueError(f"第{line_number}行:当前标签或路径为空")
            if label not in {"cat", "dog", "bird"}:
                raise ValueError(f"第{line_number}行:标签不在 cat/dog/bird")
            result = (data_path,label)
            results.append(result)
    return results

def main():

    base_dir = Path(__file__).parent

    print(read_labels(base_dir / "labels_valid.txt"))
    # print(read_labels(base_dir / "labels_invalid_label.txt"))
    # print(read_labels(base_dir / "labels_invalid_format.txt"))
    # print(read_labels(base_dir / "labels_empty_path.txt"))
    # print(read_labels(base_dir / "labels_empty_label.txt"))

if __name__ == "__main__":
    main()
