"""
为什么再次做之前做过的题目，却仍然要花那么多的时间呢？？？？？？
感觉自己，好傻逼，啊！！！！！
这种两个字符串的匹配，都是要么是深度优先，要么是动态规划
输入: S = "babgbag", T = "bag"
输出: 5
解释:

如下图所示, 有 5 种可以从 S 中得到 "bag" 的方案。
(上箭头符号 ^ 表示选取的字母)

babgbag
^^ ^
babgbag
^^    ^
babgbag
^    ^^
babgbag
  ^  ^^
babgbag
    ^^^
"""


class Solution:
    def __init__(self):
        self.count = 0

    def numDistinct1(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: int
        """
        self.func(s, t)
        return self.count

    def func(self, s, t):
        """
        添加评论
        :param s:
        :param t:
        :return:
        """
        if not t:
            self.count += 1
            return
        if not s:
            return
        for i in range(len(s)):
            if s[i] == t[0]:
                print("i is {}, s[i] is {}, t is {}".format(i, s[i], t))
                self.func(s[i + 1:], t[1:])

    def numDistinct(self, s, t):
        """
        一个问题的解可以划分为问题的子解
        要么是深度优先
        要么是动态规划
        :param s:
        :param t:
        :return:
        """
        mark = [[0 for _ in range(len(s) + 1)] for _ in range(len(t) + 1)]
        # 这个问题为什么会这样的初始化呢？
        # 因为长度为0的串，在一个任意长度的串中都存在
        for i in range(len(s) + 1):
            mark[0][i] = 1
        print(mark)
        for i in range(1, len(t) + 1):
            for j in range(1, len(s) + 1):
                if s[j - 1] == t[i - 1]:
                    mark[i][j] = mark[i - 1][j - 1] + mark[i][j - 1]
                else:
                    mark[i][j] = mark[i][j - 1]
        return mark[-1][-1]


S = 'babgbag'
T = 'bag'
s = Solution()
print(s.numDistinct(S, T))
