
from collections import Counter
import os
from pathlib import Path
import tempfile

def write_label_summary(items: list[tuple[str, str]], output_path: Path) -> None:
    output = Path(output_path)
    parent = output.parent
    if not parent.exists():
        raise FileNotFoundError(f"输出目录不存在：{parent}")

    # 例如：

    # from collections import Counter

    # counter = Counter(["cat", "dog", "cat", "bird"])

    # 得到的结果相当于：

    # {
    #     "cat": 2,
    #     "dog": 1,
    #     "bird": 1
    # }
    couter = Counter(label for _,label in items)

    # 创建临时文件
    fd,temp_path = tempfile.mkstemp(
        dir = parent,
        prefix = f".{output.name}.",
        text = True
    )

    try:
        with open(fd,"w",encoding = "utf-8") as file:
            file.write("label\tcount\n")

            for label in sorted(couter):
                file.write(f"{label}\t{couter[label]}\n")
        # 临时文件替换为目标文件
        os.replace(temp_path,output)
        temp_path = None
    finally:
        # 如果中途发生异常
        if temp_path is not None:
            try:
                os.remove(temp_path)
            except FileNotFoundError:
                pass

def main():

    items = [
        ("a.jpg", "cat"),
        ("b.jpg", "dog"),
        ("c.jpg", "cat"),
        ("d.jpg", "bird"),
    ]
    base_dir = Path(__file__).parent

    write_label_summary(items,base_dir / "existing_summary.txt")
if __name__ == "__main__":
    main()
