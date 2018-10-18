"""
给定整数n，取若干个1到n的整数可求和等于整数m，编程求出所有组合的个数。比如当n=6，m=8时，有四种组合：[2,6], [3,5], [1,2,5], [1,3,4]。限定n和m小于120 

输入描述:

整数n和m
输出描述:

求和等于m的所有组合的个数。
输入例子1:

6 8
输出例子1:

4
"""


def func(n, m):
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    for j in range(n + 1):
        dp[0][j] = 1
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if i < j:
                dp[i][j] = dp[i][j - 1]
            else:
                dp[i][j] = dp[i][j - 1] + dp[i - j][j - 1]
    for line in dp:
        print(line)
    return dp[-1][-1]


print(func(6, 8))
