"""
爱德华有1个包含N个整数的数组A，他定义1个数组的美丽值为数组中所有不同整数的和。现在爱德华想知道数组A的所有连续子序列的美丽值之和。
请实现函数： int beauty_of_array(int[] array)  测试用例
1 => 1
1, 2 => 6
1, 1, 2 => 11
"""

def func(nums):
    res = 0
    mark = [[(set(), 0) for _ in range(len(nums))] for _ in range(len(nums))]
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if nums[j] in mark[i][j-1][0]:
                mark[i][j] = mark[i][j-1]
            else:
                mark[i][j] = (mark[i][j-1][0] | {nums[j]}, mark[i][j-1][1] + nums[j])
            res += mark[i][j][1]
    return res



def func2(length):
    res = 0.5
    n = 1
    while length > res:
        n += 1
        res += 1/(n+1)
    return n

print(func2(5.19))