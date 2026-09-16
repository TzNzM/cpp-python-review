
def clean_and_batch_paths(paths, batch_size=4):
    cleaned_path = []
    for path in paths:
        path = path.strip()
        if path.lower().endswith(".jpg") or path.lower().endswith(".png"):
            cleaned_path.append(path)
    batches = []
    for i in range(0,len(cleaned_path),batch_size):
        batch = cleaned_path[i:i+batch_size]
        batches.append(batch)
    return batches      

def parse_sample_name(name):
    name = name.strip()
    if not name.lower().endswith(".jpg"):
        raise ValueError("非法文件名")
    base = name[:-4]
    pos = base.rfind("_")
    if pos == -1:
        raise ValueError("格式不正确")
    label = base[:pos]
    sample_id = base[pos+1:]

    if not label:
        raise ValueError("label为空")
    if len(sample_id) != 6:
        raise ValueError("sampleId长度不符")
    if not sample_id.isdigit():
        raise ValueError("sampleId不是数字")

    return (label,int(sample_id))

def main():
    paths = [
        "  cat_0001.jpg ",
        "",
        "dog_0002.PNG",
        "README.md",
        "bird_0003.jpg",
        "fish_0004.jpeg",
        "frog_0005.png",
        "rat_0006.jpg",
        " rabbit_0007.jpg "
    ]
    batches = clean_and_batch_paths(paths)
    for batch in batches:
        print(batch)
    print(parse_sample_name("cat_000123.jpg"))             # ("cat", 123)
    print(parse_sample_name("traffic_light_000042.JPG"))   # ("traffic_light", 42)
    # print(parse_sample_name("cat_123.jpg"))               # ValueError
    # print(parse_sample_name("_000012.jpg"))                # ValueError
    print(parse_sample_name("cat_000012.png"))            # ValueError

if __name__ == "__main__":
    main()