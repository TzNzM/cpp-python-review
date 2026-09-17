def append_log_bad(message, history=[]):
    """
    向 history 追加一条 message，并返回 history。
    """
    # 1. 把 message 追加到 history
    # 2. 返回 history
    history.append(message)
    return history

def append_log(message, history=None):
    """
    向 history 追加一条 message；未传入 history 时创建新列表。
    """
    # 1. 如果 history 是 None，创建一个新空 list
    # 2. 把 message 追加到 history
    # 3. 返回 history
    if history is None:
        history = []
    history.append(message)
    return history

def main():
    first = append_log_bad("start")
    second = append_log_bad("finish")

    print(first)
    print(second)

    first = append_log("start")
    second = append_log("finish")
    
    print(first)
    print(second)


    outside = []
    result = append_log("from outside", outside)

    print(outside)
    print(result)
    print(result is outside)

if __name__ == "__main__":
    main()