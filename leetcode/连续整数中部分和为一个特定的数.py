"""
例如，n为6，那么就是[1, 2, 3, 4, 5, 6]中组合的和为m
"""


def func(n, m):
    nums = [[0 for _ in range(m)] for _ in range(n)]
    # 为什么要在这个地方赋值呢？
    # 还有就是这个地方赋值的含义是什么呢
    # 好吧，是我太傻逼了，这玩意儿，啥几把做
    for i in range(n):
        nums[i][0] = 1
    # 外层往下走
    for i in range(n):
        # 内层往右走
        for j in range(1, m):
            # 如果i>j，那么说明，i是不可能被包含的
            # 感觉这题，不管什么时候从头开始做的话，都是想不出来的
            if i > j:
                nums[i][j] = nums[i - 1][j]
            else:
                nums[i][j] = nums[i - 1][j] + nums[i - 1][j - i]
    for ele in nums:
        print(ele)


func(6, 8)
