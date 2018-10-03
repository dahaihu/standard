"""
不管怎样，都要加油的
别人挺厉害的，
但是呢，
你真的那么差吗
你的自信跑哪里去了
这一个多星期都要加油，
把你应该学的，都学完。
博客要每天都更新
"""

# 你的j好像一直都没动啊
def kmp(s, t):
    mark = func(t)
    print('mark is \n{}'.format(mark))
    i, j = 0, 0
    while j < len(s):
        print('i is {}, j is {}'.format(i, j))
        if s[i: j + 1] == t[: j - i + 1]:
            # 长度加1
            j += 1
        # 不相同的时候，要分两种情况
        else:
            # 情况1 第一个字符就不相等，这个时候mark是无用的
            if i == j:
                i = j = i+1
            else:
                # 情况2 开头部分相等，这个时候根据mark进行移动
                i += mark[j - i - 1]
        # 如果j - i 的长度的等于t的长度，说明，成功匹配。
        # 注意，这个判断是不能放在开头的。
        # 如果，如果s的最后部分，和t匹配，那么放在开头是返回的为Flase的
        if j - i == len(t):
            return True
    return False


def func(s):
    res = [0 for _ in range(len(s))]
    # i 代指的是长度
    for i in range(1, len(s) + 1):
        cur = 0
        tmp = s[:i]
        # j 也代指的是长度，代表的是
        for j in range(1, i):
            if tmp[:j] == tmp[-j:] and j > cur:
                cur = j
        res[i - 1] = i - cur
    return res


# print(func('abcdabd'))
print(kmp('bbc abcdab abcdabcdabcdabd', 'abcdabd'))
