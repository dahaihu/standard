"""

给定正整数 n，找到若干个完全平方数（比如 1, 4, 9, 16, ...）使得它们的和等于 n。你需要让组成和的完全平方数的个数最少。

示例 1:

输入: n = 12
输出: 3
解释: 12 = 4 + 4 + 4.
示例 2:

输入: n = 13
输出: 2
解释: 13 = 4 + 9.
"""


class Solution:
    """
    二叉树的最小深度
    """
    def numSquares(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n == 1:
            return 1
        mx = 1
        # mark中用于存储可以使用的平方数
        mark = []
        while mx * mx <= n:
            mark.append(mx)
            mx += 1
        print(f'mark is {mark}')
        res = {n}
        cnt = 0
        while res:
            cnt += 1
            tmp = set()
            for ele in res:
                for p in mark:
                    if ele > p:
                        tmp.add(ele-p)
                    elif ele == p:
                        return cnt
                    else:
                        break
            res = tmp

s = Solution()
print(s.numSquares(12))
