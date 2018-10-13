"""
给定两个整数 n 和 k，返回 1 ... n 中所有可能的 k 个数的组合。

示例:

输入: n = 4, k = 2
输出:
[
  [2,4],
  [3,4],
  [2,3],
  [1,2],
  [1,3],
  [1,4],
]
"""
# 感觉自己是个傻逼，为什么做过的题，还是不会做呢？
# 无语死了

class Solution:
    def combine(self, n, k):
        self.n = n
        res = []
        self.help(1, k, [], res)
        # for i in range(1, n - k + 2):
        #     self.help(i, k-1, [i], res)
        return res

    def help(self, cur, k, path, res):
        """
        :param cur: 当前的索引位置
        :param k: 还需要k个数
        :param path: 已有的路径
        :param res: 保存的结果
        :return:
        """
        if k == 0:
            res.append(path)
            return
        for i in range(cur, self.n + 1):
            self.help(i+1, k - 1, path + [i], res)


s = Solution()
print(s.combine(5, 2))
