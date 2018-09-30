"""
例如，n为6，那么就是[1, 2, 3, 4, 5, 6]中组合的和为m
"""
def func(n, m):
    nums = [[0 for _ in range(m+1)] for _ in range(n+1)]
    # 为什么要在这个地方赋值呢？
    for i in range(n+1):
        nums[i][0] = 1
    # 外层往下走
    for i in range(1, n+1):
        # 内层往右走
        for j in range(1, m+1):
            if i > j:
                nums[i][j] = nums[i-1][j]
            else:
                nums[i][j] = nums[i-1][j] + nums[i-1][j-i]
    for ele in nums:
        print(ele)

func(6, 8)
