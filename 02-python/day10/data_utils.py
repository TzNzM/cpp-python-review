from metrics import count_labels
import os
from pathlib import Path
import tempfile


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
    couter = count_labels(items)

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