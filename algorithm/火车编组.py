def func():
    # 原始
    original = list(range(1, 5))

    # # 需要转化的
    # a = [3, 2, 1]
    a = [int(input().strip()), int(input().strip()), int(input().strip()), int(input().strip())]
    stack = []
    while a:
        # stack的最后一个值和a的第一个值相等
        if stack and stack[-1] == a[0]:
            stack.pop()
            a.pop(0)
        # 不相等的话，就要
        else:
            if not original:
                return 'No'
            # 一直插入，直到original的第一个值 和 a的第一个值相同
            print("a is {}, original is {}".format(a, original))
            while a[0] != original[0]:
                stack.append(original.pop(0))
                if not original:
                    return 'No'
            a.pop(0)
            original.pop(0)
    return 'Yes'


print(func())
